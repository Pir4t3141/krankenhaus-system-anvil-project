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
def get_coordinates(krankenhaus_name: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(f"SELECT latitude, longitude FROM krankenhaus WHERE krankenhaus_id = '{krankenhaus_name}'").fetchall()
  return result

@anvil.server.callable
def get_station_info(krankenhaus_name: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(f"SELECT f.bezeichnung AS stationenfachrichtung, COUNT(z.zimmer_id) AS zimmeranzahl FROM station s JOIN fachrichtung f ON s.fachrichtung_id = f.fachrichtung_id JOIN zimmer z on z.station_id = s.station_id JOIN krankenhaus k on k.krankenhaus_id = s.krankenhaus_id WHERE k.name = {krankenhaus_name} GROUP BY s.station_id;").fetchtall()
  return [dict(row) for row in result]