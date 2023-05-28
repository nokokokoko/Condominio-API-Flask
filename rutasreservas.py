import sqlite3
import pymysql
import requests
import json
from __main__ import app
from flask import jsonify
from flask import flash, request
from settings_db import connect_to_db
from flask_cors import cross_origin

'''Funcion que llama todas las reservas existentes'''

@app.route('/reserva')
def get_reserva():
    dep = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id_reserva_ec, fecha, hora_inicio, hora_termino, ec.nombre 'NombreEC', itec.nombre 'TipoEC', d.nro_depto 'Dep', estado\
                    FROM reserva_ec JOIN departamento d on d.id_departamento = fk_id_departamento\
                    JOIN espacio_comun ec on ec.id_ec = fk_id_ec\
                    JOIN tipo_ec itec on itec.id_tipo_ec = ec.fk_id_tipo_ec")
        rows = cur.fetchall()
        for i in rows:
            deps = {}
            deps["id_reserva_ec"] = i["id_reserva_ec"]
            deps["fecha"] = i["fecha"]
            deps["hora_inicio"] = i["hora_inicio"]
            deps["hora_termino"] = i["hora_termino"]
            deps["NombreEC"] = i["NombreEC"]
            deps["TipoEC"] = i["TipoEC"]
            deps["Dep"] = i["Dep"]
            deps["estado"] = i["estado"]
            dep.append(deps)
    except Exception as e:
        print(e)

    return dep

'''Funcion que crea una reserva en base a los datos entregados'''

@app.route('/reserva/create', methods=['POST'])
def create_resv():
    try:
        if request.method == 'POST':
            fecha = request.form['fecha']
            hora_inicio = request.form['hora_inicio']
            hora_termino = request.form['hora_termino']
            espacio_comun = request.form['espacio_comun']
            id_departamento = request.form['id_departamento']
            if fecha or hora_inicio or hora_termino or espacio_comun or id_departamento =="":
                conn = connect_to_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO reserva_ec(fecha,hora_inicio,hora_termino,estado,fk_id_ec,fk_id_departamento) VALUES (?,?,?,0,?,?)",(fecha, hora_inicio, hora_termino, espacio_comun, id_departamento))
                conn.commit()
                msg = "Success!"
            else:
                msg = "Datos invalidos"
                return msg
    except:
        conn().rollback()
        msg = "Something went wrong"
    finally:
        conn.close()
        return msg

'''Funcion que consulta los datos de la tabla Anulados'''

@app.route('/anulados')
def get_anulados():
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT EMP_ID, ENTRY_DATE, FECHA, hora_inicio, hora_termino, id_departamento FROM anulados;")
        rows = cur.fetchall()
        dep = []
        for row in rows:
            emp_id = row["EMP_ID"]
            entry_date = row["ENTRY_DATE"]
            fecha = row["FECHA"]
            hora_inicio = row["hora_inicio"]
            hora_termino = row["hora_termino"]
            id_departamento = row["id_departamento"]
            dep.append({
                "emp_id": emp_id,
                "entry_date": entry_date,
                "fecha": fecha,
                "hora_inicio": hora_inicio,
                "hora_termino": hora_termino,
                "id_departamento": id_departamento
            })
        return jsonify(dep)
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while retrieving anulados."}), 500
    finally:
        cur.close()
        conn.close()

'''Funcion que elimina un registro de reserva en base al ID de esta'''

@app.route('/reserva/delete/<int:idx>', methods=['DELETE'])
@cross_origin()
def test_delete_emp(idx):
	try:
		conn = connect_to_db()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM reserva_ec WHERE id_reserva_ec = ?", (idx,))
		conn.commit()
		respone = jsonify('Reserva eliminada!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

'''Funcion que actualiza un registro con el metodo PATCH, donde se habilita
o se deshabilita una reserva'''

@app.route('/reserva/update/<int:idx>-<int:habilitacion>', methods=['PATCH'])
@cross_origin()
def test_update_emp(idx, habilitacion):
	try:
		conn = connect_to_db()
		cursor = conn.cursor()
		cursor.execute("UPDATE reserva_ec\
                                SET estado = ? \
                                WHERE id_reserva_ec = ?", (habilitacion,idx,))
		conn.commit()
		respone = jsonify('Reserva actualizada.')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
