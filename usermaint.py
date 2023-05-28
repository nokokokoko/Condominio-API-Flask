import sqlite3
import pymysql
import requests
import json
from __main__ import app
from flask import jsonify
from flask import flash, request
from settings_db import connect_to_db


'''Funcion basica para crear un usuario, no se usa en el caso pero la
use para aprender'''

@app.route('/create', methods=['POST'])
def create_user():
    try:
        if request.method == 'POST':
            rut = request.form['rut']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO usuario(rut,nombre,apellido,email) VALUES (?,?,?,?)",(rut, nombre, apellido, email))
            conn.commit()   
            inserted_user = get_user_by_id(cur.lastrowid)
            msg = "success!"
    except:
        conn().rollback()
        msg = "Something went wrong"
    finally:
        conn.close()
        return msg

'''Funcion que permite llamar a los usuarios '''

@app.route('/usuario')
def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, rut, nombre, apellido, email, nro_depto FROM usuario JOIN departamento d on d.fk_id_usuario = id_usuario;")
        rows = cur.fetchall()
        for i in rows:
            user = {}
            user["id_usuario"] = i["id_usuario"]
            user["rut"] = i["rut"]
            user["nombre"] = i["nombre"]
            user["apellido"] = i["apellido"]
            user["email"] = i["email"]
            user["nro_depto"] = i["nro_depto"]
            users.append(user)
    except:
        users = []

    return users


'''Funcion que permite llamar a un usuario en base a un ID entregado'''

@app.route('/usuario/<int:id_usuario>')
def get_user_by_id(id_usuario):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, rut, nombre, apellido, email, nro_depto FROM usuario \
                    JOIN departamento d on d.fk_id_usuario = id_usuario \
                        WHERE id_usuario = ?", (id_usuario,))
        row = cur.fetchone()
        if row is not None:
            user["id_usuario"] = row["id_usuario"]
            user["rut"] = row["rut"]
            user["nombre"] = row["nombre"]
            user["apellido"] = row["apellido"]
            user["email"] = row["email"]
            user["nro_depto"] = row["nro_depto"]
    except:
        pass
    return user

'''Funcion que permite actualizar a un usuario en base al ID entregado'''
'''Se solicitan todos los datos, ya que el metodo es PUT'''

@app.route('/update', methods=['PUT'])
def update_emp():
    try:
        if request.method == 'PUT':
            user_id = request.form['id_usuario']
            rut = request.form['rut']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            cur = conn.cursor()
            cur.execute("UPDATE  usuario \
                        SET rut = ?, nombre = ?, apellido = ?, email = ? \
                        WHERE id_usuario = ?;",(rut, nombre, apellido, email, user_id))
            conn.commit()   
            inserted_user = get_user_by_id(cur.lastrowid)
            msg = "success!"
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

'''Funcion que permite obtener la informacion de un departamento y usuario'''
@app.route('/departamento')
def get_depts():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id_departamento, nro_depto, us.nombre || ' ' || us.apellido 'nombre', us.rut 'rut', us.email 'email' \
                    from departamento join usuario us on fk_id_usuario = us.id_usuario;")
        rows = cur.fetchall()
        for i in rows:
            user = {}
            user["id_departamento"] = i["id_departamento"]
            user["nro_depto"] = i["nro_depto"]
            user["nombre"] = i["nombre"]
            user["rut"] = i["rut"]
            user["email"] = i["email"]
            users.append(user)
    except:
        users = []

    return users

