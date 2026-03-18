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
  return [dict(row) for row in result]

@anvil.server.callable
def get_einzelne_stationen_info(krankenhaus_name: str, station_id: int):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT s.station_id AS station_id, f.bezeichnung AS stationenfachrichtung, stats.zimmeranzahl, stats.bettenanzahl, COUNT(b.belegt_id) AS alle_belegungen, COUNT(CASE WHEN b.ende IS NULL THEN b.belegt_id END) AS aktuelle_belegungen, ROUND(CAST((COUNT(CASE WHEN b.ende IS NULL THEN b.belegt_id END))*100 AS DOUBLE)/stats.bettenanzahl,2) AS prozent FROM station s JOIN fachrichtung f ON s.fachrichtung_id = f.fachrichtung_id JOIN krankenhaus k ON k.krankenhaus_id = s.krankenhaus_id JOIN (SELECT station_id, COUNT(zimmer_id) AS zimmeranzahl, SUM(Bettenanzahl) AS bettenanzahl FROM zimmer GROUP BY station_id ) stats ON s.station_id = stats.station_id LEFT JOIN zimmer z ON z.station_id = s.station_id LEFT JOIN belegt b ON b.zimmer_id = z.zimmer_id WHERE k.name = '{krankenhaus_name}' AND s.station_id = {station_id} GROUP BY s.station_id, f.bezeichnung, stats.zimmeranzahl, stats.bettenanzahl;").fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_arzt_betreuer_per_station(station_id: int):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT k.name AS krankenhaus_name, s.bezeichnung AS stations_name, COUNT(DISTINCT a.arzt_id) AS anzahl_aerzte, COUNT(DISTINCT b.betreuer_id) AS anzahl_betreuer FROM station s JOIN krankenhaus k ON s.krankenhaus_id = k.krankenhaus_id LEFT JOIN arzt a ON a.station_id = s.station_id LEFT JOIN betreuer b ON b.station_id = s.station_id WHERE s.station_id = {station_id} GROUP BY s.station_id;").fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_aerzte_stats(station_id: int):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT a.arzt_id, a.vorname || ' ' || a.nachname AS name, COUNT(DISTINCT ba.behandlung_id) AS anzahl_behandlungen, COUNT(DISTINCT pa.pd_id) AS anzahl_diagnosen, COUNT(DISTINCT b.aufnahme_id) AS anzahl_betreute_aufnahmen FROM arzt a JOIN station s ON a.station_id = s.station_id JOIN krankenhaus k ON s.krankenhaus_id = k.krankenhaus_id LEFT JOIN behandlung_arzt ba ON a.arzt_id = ba.arzt_id LEFT JOIN pd_arzt pa ON a.arzt_id = pa.arzt_id LEFT JOIN behandlung b ON ba.behandlung_id = b.behandlung_id WHERE s.station_id = {station_id} GROUP BY a.arzt_id;").fetchall()
  return [dict(row) for row in result]
  
@anvil.server.callable
def get_betreuer_stats(station_id: int):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT b.betreuer_id, b.vorname || ' ' || b.nachname AS name, COUNT(DISTINCT ab.aufnahme_id) AS anzahl_betreute_aufnahmen, COUNT(DISTINCT au.patient_id) AS anzahl_verschiedene_patienten FROM betreuer b JOIN station s ON b.station_id = s.station_id JOIN krankenhaus k ON s.krankenhaus_id = k.krankenhaus_id LEFT JOIN aufnahme_betreuer ab ON b.betreuer_id = ab.betreuer_id LEFT JOIN aufnahme au ON ab.aufnahme_id = au.aufnahme_id WHERE s.station_id = {station_id} GROUP BY b.betreuer_id;").fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_count_of_artz_and_betreuer(krankenhaus_name: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT f.bezeichnung, COUNT(DISTINCT a.arzt_id) AS anzahl_aerzte, COUNT(DISTINCT b.betreuer_id) AS anzahl_betreuer FROM station s JOIN fachrichtung f ON s.fachrichtung_id = f.fachrichtung_id JOIN krankenhaus k ON s.krankenhaus_id = k.krankenhaus_id LEFT JOIN arzt a ON a.station_id = s.station_id LEFT JOIN betreuer b ON b.station_id = s.station_id WHERE k.name = '{krankenhaus_name}' GROUP BY s.station_id;").fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_krankenhaus_info(krankenhaus_name: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT k.name AS krankenhaus, (SELECT COUNT(*) FROM arzt a JOIN station s ON a.station_id = s.station_id WHERE s.krankenhaus_id = k.krankenhaus_id) AS anzahl_aerzte, (SELECT COUNT(*) FROM betreuer b JOIN station s ON b.station_id = s.station_id WHERE s.krankenhaus_id = k.krankenhaus_id) AS anzahl_pfleger, (SELECT COUNT(*) FROM zimmer z JOIN station s ON z.station_id = s.station_id WHERE s.krankenhaus_id = k.krankenhaus_id) AS anzahl_zimmer, (SELECT SUM(z.bettenanzahl) FROM zimmer z JOIN station s ON z.station_id = s.station_id WHERE s.krankenhaus_id = k.krankenhaus_id) AS gesamtbetten_kapazitaet, (SELECT COUNT(*) FROM belegt bel JOIN zimmer z ON bel.zimmer_id = z.zimmer_id JOIN station s ON z.station_id = s.station_id WHERE s.krankenhaus_id = k.krankenhaus_id AND (bel.ende IS NULL OR bel.ende > DATE('now'))) AS belegte_betten_aktuell FROM krankenhaus k WHERE k.name = '{krankenhaus_name}';").fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_patienten_info(krankenhaus_name: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT DISTINCT p.patient_id, p.vorname || ' ' || p.nachname AS name, p.svn, p.adresse FROM Patient p JOIN Aufnahme a ON p.patient_id = a.patient_id JOIN aufnahme_betreuer ab ON a.aufnahme_id = ab.aufnahme_id JOIN Betreuer b ON ab.betreuer_id = b.betreuer_id JOIN Station s ON b.station_id = s.station_id JOIN Krankenhaus k ON s.krankenhaus_id = k.krankenhaus_id WHERE k.Name = '{krankenhaus_name}' ORDER BY p.patient_id ASC;").fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_patienten_diagnosis(patient_id: int):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(f"SELECT d.Beschreibung AS diagnose, d.icd_code, d.icd_version, pd.feststelldatum, pd.schweregrad FROM Patient p JOIN Aufnahme a ON p.patient_id = a.patient_id JOIN PD pd ON a.aufnahme_id = pd.aufnahme_id JOIN Diagnose d ON pd.diagnose_id = d.diagnose_id WHERE p.patient_id = {patient_id} ORDER BY CASE WHEN pd.schweregrad = 'HOCH' THEN 1 WHEN pd.schweregrad = 'MITTEL' THEN 2 ELSE 3 END;").fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_patienten_info_alle_krankenhaueser(krankenhaus_name: str):
  with sqlite3.connect(data_files["krankenhaus.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute("SELECT DISTINCT p.patient_id, p.vorname || ' ' || p.nachname AS name, p.svn, p.adresse FROM Patient p JOIN Aufnahme a ON p.patient_id = a.patient_id JOIN aufnahme_betreuer ab ON a.aufnahme_id = ab.aufnahme_id JOIN Betreuer b ON ab.betreuer_id = b.betreuer_id JOIN Station s ON b.station_id = s.station_id JOIN Krankenhaus k ON s.krankenhaus_id = k.krankenhaus_id ORDER BY p.patient_id ASC;").fetchall()
  return [dict(row) for row in result]