import sqlite3
import pymysql
import requests
import json
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

import rutasreservas
import rutasCliente
import usermaint
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()

    
