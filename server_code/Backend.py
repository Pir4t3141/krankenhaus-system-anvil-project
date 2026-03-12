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
    result = cur.execute(f"SELECT latitude, longitude FROM krankenhaus WHERE name = '{krankenhaus_name}'").fetchall()
  return result

@anvil.server.callable
def get_station_info(krankenhaus_name: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT s.station_id, f.bezeichnung AS stationenfachrichtung, COUNT(z.zimmer_id) AS zimmeranzahl FROM station s JOIN fachrichtung f ON s.fachrichtung_id = f.fachrichtung_id JOIN zimmer z ON z.station_id = s.station_id JOIN krankenhaus k ON k.krankenhaus_id = s.krankenhaus_id WHERE k.name = '{krankenhaus_name}' GROUP BY s.station_id;").fetchall()
    print(result)  
  return [dict(row) for row in result]

@anvil.server.callable
def get_einzelne_stationen_info(krankenhaus_name: str, station_id: int):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT s.station_id AS station_id, f.bezeichnung AS stationenfachrichtung, stats.zimmeranzahl, stats.bettenanzahl, COUNT(b.belegt_id) AS alle_belegungen, COUNT(CASE WHEN b.ende IS NULL THEN b.belegt_id END) AS aktuelle_belegungen, ROUND(CAST((COUNT(CASE WHEN b.ende IS NULL THEN b.belegt_id END))*100 AS DOUBLE)/stats.bettenanzahl,2) AS prozent FROM station s JOIN fachrichtung f ON s.fachrichtung_id = f.fachrichtung_id JOIN krankenhaus k ON k.krankenhaus_id = s.krankenhaus_id JOIN (SELECT station_id, COUNT(zimmer_id) AS zimmeranzahl, SUM(Bettenanzahl) AS bettenanzahl FROM zimmer GROUP BY station_id ) stats ON s.station_id = stats.station_id LEFT JOIN zimmer z ON z.station_id = s.station_id LEFT JOIN belegt b ON b.zimmer_id = z.zimmer_id WHERE k.name = '{krankenhaus_name}' AND s.station_id = {station_id} GROUP BY s.station_id, f.bezeichnung, stats.zimmeranzahl, stats.bettenanzahl;").fetchall()
    print(result)  
  return [dict(row) for row in result]