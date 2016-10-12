from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, relation, sessionmaker
from sqlalchemy import create_engine, Column, Unicode, UnicodeText, Integer, \
BigInteger, String, Text, DateTime, Boolean, ForeignKey, Table
import _mysql

db_name = "twitter-political-dataset"
db_host = "localhost"
db_user = "root"
db_pass = "root"

UTF8Text = Text(collation="utf8mb4_unicode_ci", convert_unicode=True)

def create_db():
    db = _mysql.connect(db_host, user=db_user, passwd=db_pass)
    db.query("CREATE DATABASE IF NOT EXISTS `twitter-political-dataset`;")


create_db()

Base = declarative_base()

