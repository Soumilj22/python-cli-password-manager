#------------IMPORTS-----------------
from cryptography.fernet import Fernet
import json
import os

#-------KEY GENERATION---------------
def generate_key():
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key","rb").read()

if not os.path.exists("key.key"):
    generate_key()

key = load_key()
cipher = Fernet(key)

#-----------FILE SETUP---------------
FILE = "password.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    
    with open(FILE,"r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE,"w") as f:
        json.dump(data,f)    

#----------ADD PASSWORD---------------
def add_password():
    website = input("Website : ")
    username = input("Username : ")
    password = input("Password : ")

    encrypted = cipher.encrypt(password.encode()).decode()

    data = load_data()

    data[website] = {
        "username":username,
        "password":encrypted
    }

    save_data(data)

    print("Password saved!")

#------------VIEW PASSWORD-------------
def view_password():
    website = input("Enter website : ")

    data = load_data()

    if website not in data:
        print("No entry found.")
        return 

    encrypted = data[website]["password"]
    decrypted = cipher.decrypt(encrypted.encode()).decode()

    print("Username : ", data[website]["username"])
    print("Password : ", decrypted)    

#--------------LIST ACCOUNTS------------
def list_accounts():
    data = load_data()

    if not data:
        print("No accounts saved.")
        return 

    for site in data:
        print("-", site) 

#-------------MAIN MENU-----------------
while True:

    print("\n Password Manager")
    print("1. Add Password")
    print("2. View password")
    print("3. List Accounts")
    print("4. Exit")

    choice = input("Choose : ")

    if choice == "1":
        add_password()

    elif choice == "2":
        view_password()

    elif choice == "3":
        list_accounts()

    elif choice == "4":                                  # remember that choice == "1" not 1.
        break

    else:
        print("Invalid choice")
            

    