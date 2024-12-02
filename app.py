from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify


import functools



app = Flask(__name__)
app.secret_key = 'yerqrgerywefgredgetrrhgohohtg' 
app.config['SESSION_TYPE'] = 'filesystem'


logged_in_ips = {}

from route.seguridad import obtener_direccion_ip
from route.sesion import login
from route.administrado import administrador
from route.usuario import agregarUsuario
from route.cambiarContra import cambiar_contraseña
from route.familia import familia
from route.inicio import inicio
#import route.conexion_arc










