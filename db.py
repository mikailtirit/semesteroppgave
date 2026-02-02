import os
from app import app, db, User, Asset

# Denne koden tvinger scriptet til å finne databasen inni 'instance' mappen
with app.app_context():
    print("\n" + "="*50)
    print("--- IINVENTORY DATABASE REPORT ---")
    print("="*50)

    # Sjekker brukere
    print("\n[ REGISTERED USERS ]")
    try:
        alle_brukere = User.query.all()
        if not alle_brukere:
            print("No users found.")
        for u in alle_brukere:
            # Viser ID, Navn og starten på det hasha passordet
            print(f"ID: {u.id:<3} | Username: {u.username:<15} | Hash: {u.password[:20]}...")
    except Exception as e:
        print(f"Error reading users: {e}")

    # Sjekker utstyr
    print("\n[ IT ASSETS IN STORAGE ]")
    try:
        assets = Asset.query.all()
        if not assets:
            print("Inventory is empty.")
        else:
            for a in assets:
                print(f"ID: {a.id:<3} | Name: {a.navn:<15} | Type: {a.type:<10} | SN: {a.sn}")
    except Exception as e:
        print(f"Error reading assets: {e}")

    print("\n" + "="*50 + "\n")