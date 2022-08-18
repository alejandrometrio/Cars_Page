from flask import render_template, redirect, session, request, flash 
from flask_app import app

from flask_app.models.users import User

from flask_app.models.appointment import Appointment

@app.route('/new/appointment')
def new_appointment():
    if 'usuario_id' not in session: 
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario)
    
    date = Appointment.today()
    
    return render_template('add_appointment.html', user=user, today=date)

@app.route('/create/appointment', methods=['POST'])
def create_appointment():
    if 'usuario_id' not in session: 
        return redirect('/')
    
    if not Appointment.validate_appointment(request.form): 
        return redirect('/new/appointment')

    Appointment.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/appointment/<int:id>')
def edit_appointment(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario)

    formulario_appointment = { "id": id }
    appointment = Appointment.get_by_id(formulario_appointment)
    
    date = Appointment.today()

    return render_template('edit_appointment.html', user=user, appointment=appointment, today = date)

@app.route('/update/appointment', methods=['POST'])
def update_appointment():
    if 'usuario_id' not in session:
        return redirect('/')
    
    if not Appointment.validate_appointment(request.form):
        return redirect('/edit/appointment/'+request.form['id'])

    Appointment.update(request.form)

    return redirect('/dashboard')



@app.route('/delete/appointment/<int:id>')
def delete_appointment(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario = {"id": id}
    Appointment.delete(formulario)

    return redirect('/dashboard')
