import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

@anvil.server.callable
def get_krankenhaeuser():
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM krankenhaus").fetchall()
  return result

@anvil.server.callable
def get_coordinates(krankenhausname: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(f"SELECT latitude, longitude FROM krankenhaus WHERE name = '{krankenhausname}'").fetchall()
  return result