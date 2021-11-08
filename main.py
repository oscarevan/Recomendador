import psycopg2
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret"
app.PERMANENT_SESSION_LIFETIME = timedelta(days=5)

@app.route('/', methods=["GET","POST"])
def principal():
	if request.method == 'POST':
		busqueda_maestro=request.form['busqueda_input']
		if busqueda_maestro=="Ella":
			flash("No te quiere")
		elif busqueda_maestro=="Thelmagod":
			flash("Es mi pastora, nada me faltará")
	return render_template("main.html")

if __name__ == '__main__':
	app.run(port = 2000, debug = True)