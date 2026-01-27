from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)

# her forteller vi Flask at vi skal bruke en SQLite-fil som heter database.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Dette forteller Python hvilke "bokser" vi skal ha i databasen vår. 
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True) #gir hver ting unikt nummer
    navn = db.Column(db.String(100)) # Navnet på Pc-en
    type = db.Column(db.String (50)) # Hva det er f.eks. bærbar)
    sn = db.Column(db.String(100)) # Serienummeret

# Her lager vi malen som bestemmer hva vi skal lagre om hvær bruker
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Hvert person får sin egen id
    username = db.Column(db.String(50), unique=True, nullable=False) #N Navnet du bruker for å logge inn
    password = db.Column(db.String(100), nullable=False) #Passordet ditt
    

# Denne linjen lager selve filen database.db 
with app.app_context():
    db.create_all()


# viser frem alt som er lagret i databasen 
@app.route('/')
def home():
    alle_ting = Asset.query.all()
    return render_template ('index.html', assets=alle_ting)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        ny_ting = Asset(navn=request.form['navn'], type=request.form['type'], sn = request.form['sn'])
        db.session.add(ny_ting)
        db.session.commit()
        return redirect ('/')
    return render_template ('add_asset.html')
    

# starter Flask serveren 
if __name__ == '__main__':
    app.run(debug=True)