from app import app, db, User, Asset

with app.app_context():

    print("\n--- REGISTERED USERS ---")
    alle_brukere = User.query.all()
    for u in alle_brukere:
        # Her er rettelsen: u.password (siden det er navnet i User-klassen din)
        print(f"ID: {u.id} | Name: {u.username:<12} | Password: {u.password[:25]}... ")

    print("\n--- IT ASSETS IN STORAGE ---")
    assets = Asset.query.all()
    
    if not assets:
        print("Inventory is empty. No items registered yet.")
    else:
        for a in assets:
            print(f"ID: {a.id} | {a.navn:<15} | Type: {a.type:<10} | SN: {a.sn} ")
    
    # Jeg flyttet denne ut av "else" så den alltid avslutter pent
    print("-" * 50 + "\n")