import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime

# =========================================================
# SQL INJECTION PROTECTION SYSTEM
# =========================================================

# =========================================================
# GENERATE AES-256 KEY
# =========================================================

try:

    with open("secret.key", "rb") as key_file:

        secret_key = key_file.read()

except:

    secret_key = Fernet.generate_key()

    with open("secret.key", "wb") as key_file:

        key_file.write(secret_key)

# =========================================================
# ENCRYPTION ENGINE
# =========================================================

cipher = Fernet(secret_key)

# =========================================================
# DATABASE CONNECTION
# =========================================================

connection = sqlite3.connect("users.db")

cursor = connection.cursor()

# =========================================================
# CREATE TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    encrypted_password TEXT,
    capability_code TEXT,
    created_time TEXT
)
""")

connection.commit()

# =========================================================
# ENCRYPT FUNCTION
# =========================================================

def encrypt_data(data):

    encrypted = cipher.encrypt(data.encode())

    return encrypted.decode()

# =========================================================
# DECRYPT FUNCTION
# =========================================================

def decrypt_data(data):

    decrypted = cipher.decrypt(data.encode())

    return decrypted.decode()

# =========================================================
# REGISTER USER
# =========================================================

def register_user():

    print("\n================================================")
    print("                USER REGISTRATION")
    print("================================================")

    username = input("\nEnter Username : ").strip()

    password = input("Enter Password : ").strip()

    capability_code = input(
        "Enter Secret Capability Code : "
    ).strip()

    if username == "" or password == "" or capability_code == "":

        print("\n❌ All Fields Are Required")

        return

    # =====================================================
    # SQL INJECTION PROTECTION
    # =====================================================

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        print("\n⚠ Username Already Exists")

        return

    # =====================================================
    # AES-256 ENCRYPTION
    # =====================================================

    encrypted_password = encrypt_data(password)

    encrypted_capability = encrypt_data(capability_code)

    created_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # =====================================================
    # INSERT SECURE DATA
    # =====================================================

    cursor.execute("""
    INSERT INTO users VALUES (?, ?, ?, ?)
    """, (
        username,
        encrypted_password,
        encrypted_capability,
        created_time
    ))

    connection.commit()

    print("\n✅ User Registered Securely")

# =========================================================
# LOGIN USER
# =========================================================

def login_user():

    print("\n================================================")
    print("                   USER LOGIN")
    print("================================================")

    username = input("\nEnter Username : ").strip()

    password = input("Enter Password : ").strip()

    capability_code = input(
        "Enter Capability Code : "
    ).strip()

    # =====================================================
    # SQL INJECTION SAFE QUERY
    # =====================================================

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    if user:

        stored_password = decrypt_data(user[1])

        stored_capability = decrypt_data(user[2])

        # =================================================
        # DOUBLE LAYER SECURITY
        # =================================================

        if (
            password == stored_password and
            capability_code == stored_capability
        ):

            print("\n✅ Secure Login Successful")

            print(f"\n🕒 Login Time : {datetime.now()}")

        else:

            print("\n❌ Invalid Credentials")

    else:

        print("\n❌ User Not Found")

# =========================================================
# VIEW USERS (ADMIN PURPOSE)
# =========================================================

def view_users():

    print("\n================================================")
    print("              SECURE USER DATABASE")
    print("================================================")

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    if not users:

        print("\n❌ No Users Found")

        return

    for user in users:

        print(f"""
------------------------------------------------
👤 Username : {user[0]}
🔒 Encrypted Password : {user[1]}
🛡 Capability Code : {user[2]}
🕒 Created Time : {user[3]}
------------------------------------------------
""")

# =========================================================
# MAIN LOOP
# =========================================================

while True:

    print("\n================================================")
    print("       SQL INJECTION PROTECTION SYSTEM")
    print("================================================")

    print("\n1. Register User")
    print("2. Login User")
    print("3. View Secure Database")
    print("4. Exit")

    choice = input("\nEnter Your Choice : ").strip()

    # =====================================================
    # REGISTER
    # =====================================================

    if choice == "1":

        register_user()

    # =====================================================
    # LOGIN
    # =====================================================

    elif choice == "2":

        login_user()

    # =====================================================
    # VIEW USERS
    # =====================================================

    elif choice == "3":

        view_users()

    # =====================================================
    # EXIT
    # =====================================================

    elif choice == "4":

        print("\n🚪 Program Closed")

        connection.close()

        break

    # =====================================================
    # INVALID OPTION
    # =====================================================

    else:

        print("\n❌ Invalid Choice")