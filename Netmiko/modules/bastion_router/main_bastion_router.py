# modules/bastion_router/main_bastion_router.py
from .connect_bastion import connect_to_bastion  # Import relativo al mismo paquete

from .sync_bastion_db import sync_bastion_interfaces

def main():
    print("🔹 Syncing Bastion interfaces with database...")
    sync_bastion_interfaces()




def main():
    print("🔹 Connecting to Bastion and retrieving interfaces...")
    output = connect_to_bastion()
    if output:
        print("\n🔹 Interfaces on Bastion:")
        print(output)
    else:
        print("❌ Could not retrieve interfaces.")

if __name__ == "__main__":
    main()
