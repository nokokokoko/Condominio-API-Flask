import sqlite3
import pymysql
import requests
import json
from __main__ import app
from flask import jsonify
from flask import flash, request
from settings_db import connect_to_db


'''Funcion que busca una reserva en base a los siguientes datos:
    Fecha y espacio comun a solicitar'''

@app.route('/reserva/cliente/<string:fecha>/<string:espacioC>')
def get_reservaCliente(fecha, espacioC):
    dep = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT fecha, hora_inicio, hora_termino, ec.nombre 'NombreEC', itec.nombre 'TipoEC' \
                    FROM reserva_ec \
                    JOIN espacio_comun ec on ec.id_ec = fk_id_ec\
                    JOIN tipo_ec itec on itec.id_tipo_ec = ec.fk_id_tipo_ec\
                    WHERE fecha = ? AND ec.nombre = ?\
                    ORDER BY fecha, hora_inicio ", (fecha,espacioC,))
        rows = cur.fetchall()
        for i in rows:
            deps = {}
            deps["fecha"] = i["fecha"]
            deps["hora_inicio"] = i["hora_inicio"]
            deps["hora_termino"] = i["hora_termino"]
            deps["NombreEC"] = i["NombreEC"]
            deps["TipoEC"] = i["TipoEC"]
            dep.append(deps)
    except Exception as e:
        print(e)

    return dep

'''Funcion que busca la ID de un espacio comun en base al nombre'''

@app.route('/ecomun/<string:nombreec>')
def get_ecomun(nombreec):
    dep = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("Select id_ec, nombre FROM espacio_comun WHERE nombre = ?", (nombreec,))
        rows = cur.fetchall()
        for i in rows:
            deps = {}
            deps["id_ec"] = i["id_ec"]
            deps["nombre"] = i["nombre"]
            dep.append(deps)
    except Exception as e:
        print(e)

    return dep
