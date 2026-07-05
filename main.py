import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import hashlib
from send2trash import send2trash # For Recycle bin 

class SecureVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Folder Lock  (v3.0)")
        self.root.geometry("500x700")

        self.vault_path = os.path.join(os.getcwd(), ".my_private_vault")
        self.db_path = os.path.join(self.vault_path, "vault_registry.json")

        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)
            os.system(f"attrib +h {self.vault_path}")

        self.setup_ui()
        self.refresh_vault_list()

    def setup_ui(self):
        # --- LOCK SECTION ---
        tk.Label(self.root, text="🔒 Lock New File/Folder", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.path_entry = tk.Entry(self.root, width=50)
        self.path_entry.pack(pady=2)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Browse Folder", command=lambda: self.browse(True)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Browse File", command=lambda: self.browse(False)).pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Set Password:").pack(pady=(10,0))
        self.pass1 = tk.Entry(self.root, show="*", width=30)
        self.pass1.pack()

        tk.Label(self.root, text="Confirm Password:").pack()
        self.pass2 = tk.Entry(self.root, show="*", width=30)
        self.pass2.pack()

        # Show/Hide Checkbutton for Locking
        self.lock_show_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Show Passwords", variable=self.lock_show_var, 
                       command=self.toggle_lock_pass).pack()

        tk.Button(self.root, text="LOCK & MOVE", bg="#e74c3c", fg="white", 
                  command=self.lock_logic, width=20).pack(pady=10)

        tk.Label(self.root, text="--------------------------------------------------").pack()

        # --- UNLOCK SECTION ---
        tk.Label(self.root, text="🔓 Vaulted Items (Select to Unlock)", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.vault_list = tk.Listbox(self.root, width=60, height=8)
        self.vault_list.pack(pady=5)

        tk.Label(self.root, text="Enter Password for Selected Item:").pack()
        self.unlock_pass = tk.Entry(self.root, show="*", width=30)
        self.unlock_pass.pack()

        # Show/Hide Checkbutton for Unlocking
        self.unlock_show_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Show Password", variable=self.unlock_show_var, 
                       command=self.toggle_unlock_pass).pack()

        tk.Button(self.root, text="UNLOCK & RESTORE", bg="#2ecc71", fg="white", 
                  command=self.unlock_logic, width=20).pack(pady=10)

    # --- UI Logic Functions ---
    def toggle_lock_pass(self):
        char = "" if self.lock_show_var.get() else "*"
        self.pass1.config(show=char)
        self.pass2.config(show=char)

    def toggle_unlock_pass(self):
        char = "" if self.unlock_show_var.get() else "*"
        self.unlock_pass.config(show=char)

    def browse(self, is_folder):
        path = filedialog.askdirectory() if is_folder else filedialog.askopenfilename()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def refresh_vault_list(self):
        self.vault_list.delete(0, tk.END)
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                data = json.load(f)
                for filename in data.keys():
                    self.vault_list.insert(tk.END, filename)

    # --- Core Logic ---
    def lock_logic(self):
        source = self.path_entry.get()
        p1 = self.pass1.get()
        p2 = self.pass2.get()

        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Select a valid path!")
            return
        if not p1 or p1 != p2:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            filename = os.path.basename(source)
            dest = os.path.join(self.vault_path, filename)
            
            data = {}
            if os.path.exists(self.db_path):
                with open(self.db_path, "r") as f:
                    data = json.load(f)
            
            data[filename] = {
                "original_path": source,
                "password": self.hash_password(p1),
                "attempts": 0  # Initial attempts 0
            }

            with open(self.db_path, "w") as f:
                json.dump(data, f)

            shutil.move(source, dest)
            messagebox.showinfo("Success", f"{filename} locked!\nMax attempts: 20")
            
            self.path_entry.delete(0, tk.END)
            self.pass1.delete(0, tk.END)
            self.pass2.delete(0, tk.END)
            self.refresh_vault_list()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def unlock_logic(self):
        selected_index = self.vault_list.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Select a file first!")
            return

        filename = self.vault_list.get(selected_index)
        input_pass = self.unlock_pass.get()

        with open(self.db_path, "r") as f:
            data = json.load(f)

        file_data = data.get(filename)
        hashed_input = self.hash_password(input_pass)

        if file_data and hashed_input == file_data['password']:
            # Success logic
            try:
                orig_path = file_data['original_path']
                vault_file = os.path.join(self.vault_path, filename)
                
                if not os.path.exists(os.path.dirname(orig_path)):
                    orig_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)

                shutil.move(vault_file, orig_path)
                
                del data[filename]
                with open(self.db_path, "w") as f:
                    json.dump(data, f)

                messagebox.showinfo("Success", f"Restored to: {orig_path}")
                self.unlock_pass.delete(0, tk.END)
                self.refresh_vault_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            # Wrong Password - Attempt Logic
            file_data['attempts'] += 1
            remaining = 20 - file_data['attempts']
            
            if file_data['attempts'] >= 20:
                # Self-destruct logic (Move to Recycle Bin)
                vault_file = os.path.join(self.vault_path, filename)
                send2trash(vault_file) # Sends to Recycle Bin
                
                del data[filename]
                with open(self.db_path, "w") as f:
                    json.dump(data, f)
                
                messagebox.showerror("Self Destruct", f"20 failed attempts! '{filename}' has been moved to Recycle Bin.")
                self.refresh_vault_list()
            else:
                with open(self.db_path, "w") as f:
                    json.dump(data, f)
                messagebox.showerror("Denied", f"Wrong Password!\nAttempts remaining: {remaining}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureVaultApp(root)
    root.mainloop()