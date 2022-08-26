from flask import render_template, redirect, session, request, flash #importaciones de módulos de flask
from flask_app import app

#Importar el modelo de User
from flask_app.models.users import User

#Importar el modelo de Receta
from flask_app.models.recipes import Recipe

#Ruta que tiene el nuevo formulario esta en el (dashboard)
@app.route('/new/recipe')
def new_recipe():
    #permite que solo  usurios que inicio sesion  pueda ver la pagina
    if 'usuario_id' not in session:
        return redirect('/')
    # este formulario viene de user_controller 
    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario)
    
    return render_template('new_recipe.html', user=user)


#Esta accion de create/recipe esta new_recipe.html
@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    #Tengo que validar mi receta
    if not Recipe.valida_receta(request.form): #Recipe.valida_receta(ENVIA FORMULARIO a recipe.py). SI NO ES VALIDO entonces:
        return redirect('/new/recipe')

    #Si esta todo bien entonces:
    Recipe.save(request.form)
    # y se redirrecciona al dashboard
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>') #Recibo el identificador de la receta que quiero editar
def edit_recipe(id):
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario) #Usuario que inició sesión

    formulario_receta = { "id": id }
    #llamar a una función y debo de recibir la receta
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id']) #/edit/recipe/1

    Recipe.update(request.form)

    return redirect('/dashboard')

@app.route('/show/recipe/<int:id>') #A través de la URL recibimos el ID de la receta
def show_recipe(id):
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario) #Usuario que inició sesión


    formulario_receta = { "id": id }
    #llamar a una función y debo de recibir la receta
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('show_recipe.html', user=user, recipe=recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'usuario_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Recipe.delete(formulario)

    return redirect('/dashboard')