from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash as hash_pw, check_password_hash as sjekk_pw

app = Flask(__name__)

# Forteller Flask at vi bruker en database-fil som heter database.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Bestemmer hva vi skal lagre om utstyr (PC-er, utstyr osv.)
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)           
    navn = db.Column(db.String(100))                      
    type = db.Column(db.String(50))                     
    sn = db.Column(db.String(100))                         

# Bestemmer hva vi skal lagre om hver bruker (innlogging)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)               
    username = db.Column(db.String(50), unique=True, nullable=False) 
    password = db.Column(db.String(200), nullable=False)    

# Lager selve databasen hvis den ikke finnes fra før
with app.app_context():
    db.create_all()

# 1. FORSIDEN (Viser innloggingsskjemaet)
@app.route('/')
def home():
    return render_template('index.html')

# 2. REGISTRERING (Lager en ny bruker i databasen)
@app.route('/register', methods=['POST'])
def register():
    brukernavn = request.form.get('username')               
    passord = request.form.get('password')                     
    
    if brukernavn and passord:
        # Sjekker om navnet er ledig før vi lager brukeren
        if not User.query.filter_by(username=brukernavn).first():
            ny_bruker = User(username=brukernavn, password=hash_pw(passord, method='pbkdf2:sha256'))
            db.session.add(ny_bruker)                  
            db.session.commit()                                
            print(f"*** NY BRUKER LAGRET: {brukernavn} ***")
            
    return redirect(url_for('home'))                       

# 3. LOGG INN (Sjekker om brukernavn og passord stemmer)
@app.route('/login', methods=['POST'])
def login():
    brukernavn = request.form.get('username')
    passord = request.form.get('password')
    
    bruker = User.query.filter_by(username=brukernavn).first() 
    
    # Sjekker om brukeren finnes og om passordet stemmer
    if bruker and sjekk_pw(bruker.password, passord):
        print(f"--- LOGG INN: {brukernavn} er inne ---")
        return redirect(url_for('welcome'))                 
    
    print(f"--- FEIL: Innlogging feilet for {brukernavn} ---")
    return redirect(url_for('home'))                          

# 4. VELKOMSTSIDEN (Siden man ser etter innlogging)
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    app.run(debug=True)