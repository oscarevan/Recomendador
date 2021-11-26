import psycopg2
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret"
app.PERMANENT_SESSION_LIFETIME = timedelta(days=5)

conexion = psycopg2.connect(
	host = "localhost",
	database = "el_recomendador",
	user = "postgres",
	password = "evanilson20")

cursor = conexion.cursor()

@app.route('/', methods=["GET","POST"])
@app.route('/<usuario>', methods=["GET","POST"])
def main(usuario="Registrarte / Iniciar Sesión"):
	if "user" in session:
		usuario = session['user']
	if request.method == 'POST':
		busqueda_maestro=request.form['busqueda_input']
		if busqueda_maestro!="":
			return redirect(url_for("maestros", resultado=busqueda_maestro))
	return render_template("main.html", usuario=usuario)

@app.route('/agregar_profesor', methods=["GET", "POST"])
def agregar_profesor():
	if "user" in session:
		if request.method == 'POST':
			agregar_profesor=request.form['agregar_input']

			cursor.execute("insert into peticiones values ('{0}')".format(agregar_profesor))
			conexion.commit()

			flash("Petición enviada, en proceso de revisión")
			return redirect(url_for("main"))

		return render_template("agregar_profesor.html", usuario=session["user"])
	return redirect(url_for("iniciar_sesion"))

@app.route('/iniciar_sesion', methods=["GET", "POST"])
def iniciar_sesion():
	if request.method == 'POST':
		correo=request.form['correo']
		password=request.form['password']
		password = hashlib.md5(password.encode())
		password = password.hexdigest()

		cursor.execute("select * from usuario where correo = %s and contrasena = %s", (correo, password))
		rows = cursor.fetchall()

		for r in rows:
			if r[1] == correo and r[2] == password:
				session['user'] = r[0]
				flash("Hola de nuevo, te extrañamos")
			return redirect(url_for("main"))
		else:
			flash("Datos incorrectos, vuelva a intentarlo")

	if "user" in session:
		return redirect(url_for("usuario"))
	return render_template("inicio_sesion.html")

@app.route('/usuario', methods=["GET", "POST"])
def usuario():
	if "user" in session:
		cursor.execute("select correo from usuario where username = '{0}'".format(session["user"]))
		correo_lista = cursor.fetchone()
		correo = correo_lista[0]
		return render_template("usuario.html", usuario=session["user"], correo=correo)
	else:
		return redirect(url_for("main"))

@app.route('/crear_cuenta', methods=["GET", "POST"])
def crear_cuenta():
	if request.method == 'POST':
		usuario = request.form['usuario']
		correo = request.form['correo']
		password = request.form['password']
		confirmar_password = request.form['confirmar_password']

		cursor.execute("select username,correo from usuario")
		user = cursor.fetchall()

		bandera = False
		bandera_correo = False

		for u in user:
			if usuario == u[0]:
				bandera = True
			if correo == u[1]:
				bandera_correo = True

		if bandera:
			flash("Usuario ya registrado, vuelva a intentarlo")
		elif bandera_correo:
			flash("Correo electrónico ya registrado, vuelva a intentarlo")
		elif correo.find('@') == -1:
			flash("Correo inválido, vuelva a intentarlo")
		elif len(password)<5 or len(password)>21:
			flash("La contraseña debe contener de 6 a 20 caracteres")
		elif password != confirmar_password:
			flash("Las contraseñas no coinciden, vuelva a intentarlo")
		else:
			password = hashlib.md5(password.encode())
			password = password.hexdigest()
			cursor.execute("insert into usuario values (%s,%s,%s)", (usuario,correo,password))
			conexion.commit()
			session['user'] = usuario
			flash("¡Bienvenido!")
			return redirect(url_for("main"))
	return render_template("crear_cuenta.html")

@app.route('/borrar_comentario')
def borrar_comentario():
	return redirect(url_for("profesor"))

@app.route('/maestros/<resultado>', methods=["GET", "POST"])
def maestros(resultado):
	if "user" in session:
		usuario = session["user"]
	else:
		usuario = ''

	resultado = str(resultado)
	arreglo = resultado.split()
	resultado = ''
	for cadena in arreglo:
		resultado += cadena.capitalize()
		resultado += ' '
	resultado = resultado[:-1]

	#Se busca resultado en la base de datos y los resultados se agregan a la lista mostrar en html
	cursor.execute("select * from profesor where nombre like '%{0}%'".format(resultado))
	tupla = cursor.fetchall()
	lista = []
	busqueda = '(profesor)'

	if len(tupla) == 0:
		cursor.execute("select * from profesor as p join resena as m on p.id = m.profesorid where materia != 'Desconocida' and materia like '%{0}%'".format(resultado))
		tupla = cursor.fetchall()
		busqueda = '(materia)'

	for maestros in tupla:
		maestro = []
		for elemento in maestros:
			maestro.append(elemento)
		lista.append(maestro)

	for maestro in lista:
		if maestro[2] is None:
			maestro[2] = "Sin calificación"

	if len(tupla) == 0:
		flash("No se encontraron resultados")
		busqueda = ''

	if request.method == 'POST':
		id_profesor = request.form['id']
		return redirect(url_for("profesor", id_profesor=id_profesor))
	return render_template("maestros.html", resultado=resultado, lista=lista, usuario=usuario, busqueda=busqueda)

@app.route('/profesor/<id_profesor>', methods=["GET", "POST"])
def profesor(id_profesor):

	if "user" in session:
		usuario = session["user"]
	else:
		usuario = ''

	id_profesor = int(id_profesor)

	cursor.execute("select nombre, calificacion from profesor where id = '{0}'".format(id_profesor))
	tupla = cursor.fetchone()
	nombre = []

	for elemento in tupla:
		nombre.append(elemento)

	if nombre[1] is None:
		nombre[1] = 'Sin calificación'

	cursor.execute("select * from califica where profesor_id = '{0}'".format(id_profesor))
	lista_profesor = cursor.fetchall()

	puntualidad = 0
	dificultad = 0
	dominio = 0
	evaluaciones = 0

	for calificaciones in lista_profesor:
		puntualidad += calificaciones[0]
		dificultad += calificaciones[1]
		dominio += calificaciones[2]
		evaluaciones += 1

	if evaluaciones != 0:
		puntualidad = puntualidad/evaluaciones
		dificultad = dificultad/evaluaciones
		dominio = dominio/evaluaciones

		puntualidad = round(puntualidad, 2)
		dificultad = round(dificultad, 2)
		dominio = round(dominio, 2)

	lista_calificacion = [puntualidad,dificultad,dominio,evaluaciones]

	cursor.execute("select * from resena where profesorid = '{0}'".format(id_profesor))
	comentarios_profesor = cursor.fetchall()

	if request.method == 'POST':
		if "user" in session:
			id_profesor = request.form['id'] 
			return redirect(url_for("calificar_profesor", id_profesor=id_profesor))
		else:
			return redirect(url_for("iniciar_sesion"))

	return render_template("profesor.html", nombre=nombre, lista=lista_calificacion, id_profesor=id_profesor, comentarios=comentarios_profesor, usuario=usuario)

@app.route('/calificar_profesor/<id_profesor>', methods=["GET", "POST"])
def calificar_profesor(id_profesor):

	if "user" in session:
		usuario = session["user"]
	else:
		usuario = ''

	id_profesor = int(id_profesor)

	cursor.execute("select nombre from profesor where id = '{0}'".format(id_profesor))
	nombre = cursor.fetchone()

	if request.method=='POST':
		materia = request.form['materia']
		materia = materia.capitalize()
		if len(materia) == 0 or materia[0] != 'I':
			materia = "Desconocida"

		puntualidad = int(request.form['puntualidad'])
		dificultad = int(request.form['dificultad'])
		dominio = int(request.form['dominio'])
		comentario = request.form['comentario']

		cursor.execute("select * from califica where profesor_id = %s and usuario_username = %s",(id_profesor,session["user"]))
		validacion = cursor.fetchall()

		if len(validacion) == 0:
			cursor.execute("insert into califica values (%s,%s,%s,%s,%s)", (puntualidad,dificultad,dominio,session['user'],id_profesor))
			if comentario != '':
				cursor.execute("insert into resena values (%s,%s,%s,%s)", (materia, comentario, session['user'], id_profesor))
			conexion.commit()
			flash("Gracias por tu opinión")
			
		else:
			cursor.execute("update califica set puntualidad=%s, dificultad=%s, dominio=%s where profesor_id = %s and usuario_username = %s",(puntualidad,dificultad,dominio,id_profesor,session["user"]))
			if comentario != '':
				cursor.execute("update resena set materia=%s, comentario=%s where usuariousername=%s and profesorid=%s",(materia,comentario,session["user"],id_profesor))
			conexion.commit()
			flash("Datos actualizados")

		cursor.execute("select avg(puntualidad), avg(dominio), avg(100-dificultad) from califica where profesor_id = '{0}'".format(id_profesor))
		promedios = cursor.fetchall()
		calificacion = (promedios[0][0]+promedios[0][1]+promedios[0][2])/3
		calificacion = round(calificacion,2)
		cursor.execute("update profesor set calificacion = %s where id = %s", (calificacion, id_profesor))
		conexion.commit()
		return redirect(url_for("main"))
	return render_template("calificar.html", id_profesor=id_profesor, nombre=nombre, usuario=usuario)

@app.route('/cerrar_sesion')
def cerrar_sesion():
	session.pop("user", None)
	return redirect(url_for("main"))

if __name__ == '__main__':
	app.run(port = 2000, debug = True)

conexion.commit()

cursor.close()

conexion.close()