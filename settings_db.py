import sqlite3
import pymysql
import requests
import json
from flask import jsonify
from flask import flash, request
from __main__ import app

'''Conexion con base de datos SQLite3'''

def connect_to_db():
    conn = sqlite3.connect('condominio-1.db')
    return conn
