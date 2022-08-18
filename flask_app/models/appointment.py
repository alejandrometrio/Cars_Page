from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date

from flask import flash

class Appointment:

    def __init__(self, data):
        self.id = data['id']
        self.tasks = data['tasks']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def today(cls):
        today = date.today()
        return today

    @staticmethod
    def validate_appointment(formulario):
        es_valido = True

        if formulario['tasks'] == "":
            flash("El nombre de la receta debe tener al menos 3 caracteres", "appointment")
            es_valido = False
        
        if formulario['date'] == "":
            flash("Ingrese una fecha", "appointment")
            es_valido = False
        
        return es_valido 
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO appointments (tasks, date, status, user_id) VALUES (%(tasks)s, %(date)s, %(status)s, %(user_id)s)"
        nuevoId = connectToMySQL('esquema_appointments').query_db(query, formulario)
        return nuevoId

    
    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE appointments.id = %(id)s"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        appointment = cls(result[0])
        return appointment

    @classmethod
    def update(cls, formulario):
        query = "UPDATE appointments SET tasks = %(tasks)s, date = %(date)s, status = %(status)s WHERE id = %(id)s"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        return result
    
    @classmethod
    def get_user_appointments(cls, formulario):
        query = "SELECT * FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE users.id = %(id)s "
        results = connectToMySQL('esquema_appointments').query_db(query, formulario)
        appointment = []
        for a in results:
            appointment.append(cls(a))
        return appointment