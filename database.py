import os
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
db_uri = os.getenv('DATABASE_URI')
db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT')
db_user = os.getenv('DATABASE_USER')
db_password = os.getenv('DATABASE_PASSWORD')
db_name = os.getenv('DATABASE_NAME')

db = SQLAlchemy()
db_driver = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name, port=db_port)
