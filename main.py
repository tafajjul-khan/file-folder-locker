
import os
import subprocess
import getpass

class SecureLock:
    def __init__(self, target_path):
        self.target_path = target_path
        # Current user ka naam nikalne ke liye
        self.user = os.getlogin()

    def lock(self):
        try:
            # icacls command: current user ke liye access 'deny' karna (F = Full Access)
            # /deny statement permissions ko override kar deta hai
            cmd = f'icacls "{self.target_path}" /deny {self.user}:(F)'
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(f"Locked: {self.target_path}")
        except Exception as e:
            print(f"Error locking: {e}")

    def unlock(self):
        try:
            # /remove:d ka matlab hai 'deny' rule ko hatana
            cmd = f'icacls "{self.target_path}" /remove:d {self.user}'
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(f"Unlocked: {self.target_path}")
        except Exception as e:
            print(f"Error unlocking: {e}")

def main():
    path = input("Enter file/folder path: ").strip('"')
    if not os.path.exists(path):
        print("Invalid Path!")
        return

    password = "admin123" # Hardcoded for prototype, use hashing in production
    
    action = input("Type 'L' to Lock or 'U' to Unlock: ").upper()
    entered_pass = getpass.getpass("Enter System Password: ")

    if entered_pass == password:
        locker = SecureLock(path)
        if action == 'L':
            locker.lock()
        elif action == 'U':
            locker.unlock()
        else:
            print("Invalid Action")
    else:
        print("Wrong Password! Access Denied.")

if __name__ == "__main__":
    main()