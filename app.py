from flask import Flask,render_template,redirect,url_for, flash,request
from flask_sqlalchemy import SQLAlchemmy

from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
basedir =os.path.join(basedir,'database')
os.makedirs(db_path,exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path,'events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db = SQLAlchemy(app)

class Evento(db.model):
   id = db.column(db.integer,primary_key=True)
   nome = db.Column(db.String(200), nullLable=False)
   idade_minima = db.Column(db.integer)
   data = db.Column(db.date)
   hora = db.column(db.time)
   cep = db.Column(db.String(20))
   uf = db.Column(db.String(2))
   Cidade = db.Column(db.String(100))
   local = db.Column(db.String(200))

   def create_tables():
        try:
            with app.app_context():
                db.create_all()
        except Exception:
           db.create_all()

   

@app.route("/")
def index():
    eventos = Evento.query.order_by(Evento.data).all()
    return render_template("index.html", eventos = eventos)
@app.route("/cadastrar-evento", methods=["GET", "POST"])
def cadastrar_evento():
    if request.method == "POST":
     nome = request.form.get['evento']
     idade = request.form.get['idade']
     data_str = request.form.get['data']
     hora_str = request.form.get['hora']
     cep = request.form.get['cep']
     uf = request.form.get['uf']
     cidade = request.form.get['cidade']
     local = request.form.get['local']

    idade_val = int(idade) if idade else nome
    data_val = datetime.strptime(data_str,"%y-%m-%d").date() if data_str else None
    hora_val = datetime.strptime(hora_str,"%H:%M") .time() if hora_str else None
    evento = Evento(
       nome = nome,
       idade_minima=idade_val,
       data=data_val,
       hora=hora_val,
       cep=cep,
       uf= uf,
       cidade=cidade,
       local=local,


    )

    db.session.add(evento)
    db.session.commit()
    flash('Evento cadastrado com sucesso.')
    return redirect(url_for('index'))

    return render_template("cadastra-evento.html")

if __name__ =="__main__":
    create_tables()
    app.run(debug=True)