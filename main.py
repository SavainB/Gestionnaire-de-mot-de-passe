import os
import sqlite3
import getpass
from cryptography.fernet import Fernet

# Fonction pour générer ou récupérer la clé de chiffrement
def get_encryption_key(key_file="encryption_key.key"):
    if os.path.exists(key_file):
        with open(key_file, "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as key_file:
            key_file.write(key)
    return key

def create_database(db_name, key):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            site_name TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def encrypt(text, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text.encode())

def decrypt(text, key):
    cipher_suite = Fernet(key)
    try:
        return cipher_suite.decrypt(text).decode()
    except Exception as e:
        #print("La déchiffrement a échoué :", str(e))
        return None

def add_entry(db_name, key):
    site_name = input("Nom du site : ")
    username = input("Nom d'utilisateur : ")
    password = getpass.getpass("Mot de passe : ")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords VALUES (?, ?, ?)', (site_name, username, encrypt(password, key)))
    conn.commit()
    conn.close()
    print("Entrée ajoutée avec succès !")

def view_entries(db_name, key):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT site_name, username, password FROM passwords')
    entries = cursor.fetchall()
    conn.close()

    print("Nom du site\tNom d'utilisateur\tMot de passe")
    for entry in entries:
        decrypted_password = decrypt(entry[2], key)
        print("Mot de passe chiffré avant le déchiffrement :", entry[2])
        if decrypted_password is not None:
            print(f"{entry[0]}\t{entry[1]}\t{decrypted_password}")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("Gestionnaire de mots de passe simple")
    db_name = input("Entrez le nom de la base de données : ")
    key = get_encryption_key()

    create_database(db_name, key)

    while True:
        print("\nOptions:")
        print("1. Ajouter une nouvelle entrée")
        print("2. Voir toutes les entrées")
        print("3. Quitter")
        choice = input("Entrez votre choix : ")

        if choice == "1":
            add_entry(db_name, key)
        elif choice == "2":
            view_entries(db_name, key)
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer !")

if __name__ == "__main__":
    main()
