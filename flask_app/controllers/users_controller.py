from email import message
from flask import jsonify, render_template, redirect, session, request, flash, jsonify  #importaciones de módulos de flask
from flask_app import app

#Importando el Modelo de User
from flask_app.models.users import User

#Importamos el modelo de Recetas
from flask_app.models.recipes import Recipe

#Importando BCrypt (encriptar)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) #inicializando instancia de Bcrypt

@app.route('/')
def index():
    return render_template('index.html')

#Creando una ruta para /register
@app.route('/register', methods=['POST'])
def register():
    #request.form = {
    #   "first_name": "Elena",
    #   "last_name": "De Troya",
    #   "email": "elena@cd.com",
    #   "password": "123456",
    #}
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password']) #Me encripta el password

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #Guardando a mi usuario y recibo el ID del nuevo registro

    session['usuario_id'] = id #Guardando en sesion el identificador

    return redirect('/dashboard')


#Cuando no exista un usuario me regrese un mensaje que diga 
#email no encontrado pero ahora no por medio de flash sino por medio
#de un json (AJAX lo que hace es mediante APIS va recoje información y la recibe a traves de json sin salir de la pagina)

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user: #si user=False
        return jsonify(message="Email no encontrado") 
    
    #Comparando la contraseña encriptada con la contraseña del LOGIN
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        return jsonify(message="Password incorrecto")
    
    session['usuario_id'] = user.id

    return jsonify(message="correcto")

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario) #Usuario que inicio sesión

    recipes = Recipe.get_all() #Recibimos lista de recetas

    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route('/logout')
def logout():
    session.clear() #Elimine la sesión
    return redirect('/')