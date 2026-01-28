from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Her forteller vi Flask at vi skal bruke en SQLite-fil som heter database.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Dette forteller Python hvilke "bokser" vi skal ha i databasen vår for utstyr
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)               # gir hver ting unikt nummer
    navn = db.Column(db.String(100))                           # Navnet på PC-en
    type = db.Column(db.String(50))                            # Hva det er (f.eks. bærbar)
    sn = db.Column(db.String(100))                             # Serienummeret

# Her lager vi malen som bestemmer hva vi skal lagre om hver bruker
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)               # Hver person får sin egen id
    username = db.Column(db.String(50), unique=True, nullable=False) # Navnet for innlogging
    password = db.Column(db.String(100), nullable=False)       # Passordet ditt

# Denne linjen lager selve filen database.db
with app.app_context():
    db.create_all()

# 1. FORSIDEN (Innloggingssiden)
@app.route('/')
def home():
    return render_template('index.html')                       # Viser innloggingssiden

# 2. REGISTRERING (Lage ny bruker)
@app.route('/register', methods=['POST'])
def register():
    brukernavn = request.form.get('username')                   # Henter brukernavn fra skjemaet
    passord = request.form.get('password')                     # Henter passord fra skjemaet

    if brukernavn and passord:
        ny_bruker = User(username=brukernavn, password=passord) # Samler navn og passord
        db.session.add(ny_bruker)                              # Setter klar for lagring
        db.session.commit()                                    # Lagrer det i databasen
        print(f"*** NY BRUKER LAGRET: {brukernavn} ***")       # Vises i terminalen min

    return redirect(url_for('home'))                           # Sender brukeren tilbake til forsiden

# 3. LOGG INN (Sjekke bruker)
@app.route('/login', methods=['POST'])
def login():
    brukernavn = request.form.get('username')                   # Henter brukernavn fra skjemaet
    passord = request.form.get('password')                     # Henter passord fra skjemaet

    bruker = User.query.filter_by(username=brukernavn).first() # Leter i databasen etter navnet

    if bruker and bruker.password == passord:                  # Sjekker navn og passord
        print(f"--- LOGG INN: {brukernavn} er nå inne ---")    # Logg hos admin
        return redirect(url_for('welcome'))                    # SENDER brukeren til velkomstsiden
    else: 
        print(f"--- FEIL: Feil passord for {brukernavn} ---")  # Logg hos admin
        return "Wrong username or password"                    # Feilmelding på nettsiden

# 4. VELKOMSTSIDEN (Mellomstasjonen)
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')                     # Viser velkomstsiden

# 5. OVERSIKTEN (Viser alt utstyr)
@app.route('/assets')
def show_assets():
    alle_ting = Asset.query.all()                              # Henter alt fra Asset-tabellen
    return render_template('asset.html', assets=alle_ting)     # Viser oversikten

# 6. LEGG TIL NYTT UTSTYR
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        ny_ting = Asset(navn=request.form['navn'], type=request.form['type'], sn=request.form['sn'])
        db.session.add(ny_ting)                                # Legger til i køen
        db.session.commit()                                    # Lagrer i databasen
        return redirect(url_for('show_assets'))                # Går tilbake til oversikten
    return render_template('add_asset.html')

# Starter Flask-serveren
if __name__ == '__main__':
    app.run(debug=True)