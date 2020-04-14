import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
import sqlite3
import pandas as pd

# get env variables
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

# talk to elephantSQL
conn_elephant = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print(type(conn_elephant))

# connect to sqlite db
conn_sqlite = sqlite3.connect('rpg_db.sqlite3')
print(type(conn_sqlite))

# read a table from sqlite DB
sqlite_c = conn_sqlite.cursor()
results = sqlite_c.execute('SELECT * FROM charactercreator_character').fetchall()
print(results[:5])

# create new table
table_creation_query = """
DROP TABLE IF EXISTS charactercreator_character;
CREATE TABLE IF NOT EXISTS charactercreator_character (
  character_id SERIAL PRIMARY KEY,
  name varchar(30),
  level	integer,
  exp integer,
  hp integer,
  strength integer,
  intelligence integer,
  dexterity	integer,
  wisdom integer
);
"""
elephant_c = conn_elephant.cursor()
elephant_c.execute(table_creation_query)

# insert data
insertion_query = """
INSERT INTO charactercreator_character 
(character_id,
  name,
  level,
  exp,
  hp,
  strength,
  intelligence,
  dexterity,
  wisdom)
VALUES %s"""
elephant_c = conn_elephant.cursor()
execute_values(elephant_c, insertion_query, results)

# SAVE THE RESULTS!
conn_elephant.commit()
conn_elephant.close()
conn_sqlite.close()
