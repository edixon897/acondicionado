from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_session import Session
import functools



app = Flask(__name__)
app.secret_key = 'yerqrgerywefgredgetrrhgohohtg' 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

logged_in_ips = {}

from route.seguridad import obtener_direccion_ip, login_required
from route.sesion import login
from route.administrado import administrador
from route.usuario import agregarUsuario
from route.cambiarContra import cambiar_contraseña
from route.familia import familia
from route.inicio import inicio
from route.resumen import resumen










