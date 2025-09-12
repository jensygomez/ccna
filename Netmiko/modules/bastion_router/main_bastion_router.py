# modules/bastion_router/main_bastion_router.py

from .bastion_connection import connect_to_bastion  # Import relativo

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
