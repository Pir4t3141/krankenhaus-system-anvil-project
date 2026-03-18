#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import random
import os
from datetime import date, timedelta

DB_PATH = "krankenhaus.db"

# Konfiguration
N_KRANKENHAEUSER = 3
N_FACHRICHTUNGEN = 10
N_STATIONS_PER_HOSPITAL = (3, 6)
N_ROOMS_PER_STATION = (5, 10)
N_PATIENTS = 250
N_DOCTORS = 50
N_CARERS = 70
N_ADMISSIONS_PER_PATIENT = (1, 3)

SEED = 42

# --- Erweiterte Daten Pools ---
FIRST_NAMES = ["ANNA", "PAUL", "LEA", "NOAH", "MIA", "LEON", "LINA", "ELIAS", "MARIE", "FELIX", "SARAH", "DAVID"]
LAST_NAMES = ["MÜLLER", "SCHMIDT", "SCHNEIDER", "FISCHER", "WEBER", "WAGNER", "BECKER", "HOFFMANN", "SCHULZ"]
STATION_NAMES = ["KARDIOLOGIE", "CHIRURGIE", "RADIOLOGIE", "PÄDIATRIE", "NEUROLOGIE", "ONKOLOGIE", "UROLOGIE", "INNERE MEDIZIN", "ORTHOPÄDIE"]

# Mehr deutsche Gründe für die Aufnahme
GRUENDE_POOL = [
    "AKUTE BAUCHSCHMERZEN", "VERDACHT AUF HERZINFARKT", "GEPLANTE KNIE-OP", "SCHWINDEL UND ÜBELKEIT",
    "ATEMNOT", "KNIE-ARTHROSKOPIE", "DIABETISCHE EINSTELLUNG", "OERSCHENKELHALSBRUCH",
    "ENTBINDUNG", "NACHSORGE NACH SCHLAGANFALL", "GELENKSCHMERZEN", "BLUTHOCHDRUCK-KRISE",
    "MAGENSPIEGELUNG", "ALLERGIE-TESTUNG", "INFEKTION UNBEKANNTER URSACHE", "STURZVERLETZUNG"
]

DIAGNOSE_POOL = [
    ("I10", "ICD-10", "BLUTHOCHDRUCK"), ("E11.9", "ICD-10", "DIABETES MELLITUS"), 
    ("J18.9", "ICD-10", "PNEUMONIE"), ("S06.0", "ICD-10", "GEHIRNERSCHÜTTERUNG"),
    ("M54.5", "ICD-10", "KREUZSCHMERZ"), ("K35.8", "ICD-10", "AKUTE APPENDIZITIS")
]

TREATMENT_TEXTS = ["BLUTABNAHME", "EKG", "RÖNTGEN", "ULTRASCHALL", "VERBANDSWECHSEL", "VISITE", "MRT", "LABORUNTERSUCHUNG"]

def setup_database(conn):
    cursor = conn.cursor()
    # Tabellen ohne Foreign Keys (nur _id)
    tables = [
        "CREATE TABLE fachrichtung (fachrichtung_id INTEGER, bezeichnung TEXT)",
        "CREATE TABLE krankenhaus (krankenhaus_id INTEGER, longitude DOUBLE, latitude DOUBLE, name TEXT)",
        "CREATE TABLE station (station_id INTEGER, fachrichtung_id INTEGER, krankenhaus_id INTEGER, bezeichnung TEXT)",
        "CREATE TABLE zimmer (zimmer_id INTEGER, station_id INTEGER, bettenanzahl INTEGER)",
        "CREATE TABLE patient (patient_id INTEGER, vorname TEXT, nachname TEXT, svn INTEGER, adresse TEXT)",
        "CREATE TABLE aufnahme (aufnahme_id INTEGER, patient_id INTEGER, aufnahmedatum DATE, entlassungsdatum DATE, grund TEXT)",
        "CREATE TABLE belegt (belegt_id INTEGER, zimmer_id INTEGER, patient_id INTEGER, beginn TEXT, ende TEXT)",
        "CREATE TABLE betreuer (betreuer_id INTEGER, station_id INTEGER, vorname TEXT, nachname TEXT)",
        "CREATE TABLE aufnahme_betreuer (ab_id INTEGER, aufnahme_id INTEGER, betreuer_id INTEGER)",
        "CREATE TABLE arzt (arzt_id INTEGER, station_id INTEGER, vorname TEXT, nachname TEXT)",
        "CREATE TABLE behandlung (behandlung_id INTEGER, aufnahme_id INTEGER, datum TEXT, beschreibung TEXT)",
        "CREATE TABLE behandlung_arzt (ba_id INTEGER, behandlung_id INTEGER, arzt_id INTEGER)",
        "CREATE TABLE diagnose (diagnose_id INTEGER, icd_code TEXT, icd_version TEXT, beschreibung TEXT)",
        "CREATE TABLE pd (pd_id INTEGER, aufnahme_id INTEGER, diagnose_id INTEGER, feststelldatum TEXT, schweregrad TEXT)",
        "CREATE TABLE pd_arzt (pa_id INTEGER, pd_id INTEGER, arzt_id INTEGER)"
    ]
    for table in tables:
        cursor.execute(table)

def main():
    random.seed(SEED)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    setup_database(conn)
    
    # --- 1. Stammdaten ---
    fach_list = [(i, random.choice(STATION_NAMES)) for i in range(1, N_FACHRICHTUNGEN + 1)]
    conn.executemany("INSERT INTO fachrichtung VALUES (?, ?)", fach_list)

    unique_names = list(LAST_NAMES)
    random.shuffle(unique_names)
    hospitals = [
        (
            i, 
            random.uniform(10.0, 16.0), 
            random.uniform(46.0, 49.0), 
            f"KLINIK {unique_names[i-1]}"
        ) 
        for i in range(1, N_KRANKENHAEUSER + 1)
    ]

    conn.executemany("INSERT INTO krankenhaus VALUES (?, ?, ?, ?)", hospitals)

    # --- 2. Stationen & Zimmer ---
    stations, rooms = [], []
    s_id, z_id = 1, 1
    for h_id, _, _, _ in hospitals:
        for _ in range(random.randint(*N_STATIONS_PER_HOSPITAL)):
            stations.append((s_id, random.choice(fach_list)[0], h_id, f"STATION {s_id}"))
            for _ in range(random.randint(*N_ROOMS_PER_STATION)):
                rooms.append((z_id, s_id, random.choice([1, 2, 4])))
                z_id += 1
            s_id += 1
    conn.executemany("INSERT INTO station VALUES (?, ?, ?, ?)", stations)
    conn.executemany("INSERT INTO zimmer VALUES (?, ?, ?)", rooms)

    # --- 3. Personal (mit station_id) ---
    doctors = [(i, random.choice(stations)[0], random.choice(FIRST_NAMES), random.choice(LAST_NAMES)) for i in range(1, N_DOCTORS + 1)]
    conn.executemany("INSERT INTO arzt VALUES (?, ?, ?, ?)", doctors)

    carers = [(i, random.choice(stations)[0], random.choice(FIRST_NAMES), random.choice(LAST_NAMES)) for i in range(1, N_CARERS + 1)]
    conn.executemany("INSERT INTO betreuer VALUES (?, ?, ?, ?)", carers)

    # --- 4. Patienten & Diagnosen ---
    patients = [(i, random.choice(FIRST_NAMES), random.choice(LAST_NAMES), random.randint(1000000000, 9999999999), f"HAUPTSTRASSE {random.randint(1,200)}") for i in range(1, N_PATIENTS + 1)]
    conn.executemany("INSERT INTO patient VALUES (?, ?, ?, ?, ?)", patients)

    diagnoses = [(i, d[0], d[1], d[2]) for i, d in enumerate(DIAGNOSE_POOL, 1)]
    conn.executemany("INSERT INTO diagnose VALUES (?, ?, ?, ?)", diagnoses)

    # --- 5. Bewegungsdaten (Aufnahmen, Belegungen etc.) ---
    aufnahmen, belegungen, behandlungen, b_aerzte, pds, p_aerzte, a_betreuer = [], [], [], [], [], [], []
    a_id, bel_id, beh_id, ba_rel_id, pd_id, pa_rel_id, ab_rel_id = 1, 1, 1, 1, 1, 1, 1

    for p_id, _, _, _, _ in patients:
        for _ in range(random.randint(*N_ADMISSIONS_PER_PATIENT)):
            # Datum generieren
            start_dt = date(2025, 1, 1) + timedelta(days=random.randint(0, 420))
            
            # 15% Wahrscheinlichkeit für eine aktive Aufnahme (Enddatum NULL)
            is_active = random.random() < 0.15
            
            if is_active:
                end_str = None
                end_dt_for_log = start_dt + timedelta(days=1) # Für die Behandlungs-Logik
            else:
                end_dt = start_dt + timedelta(days=random.randint(1, 20))
                end_str = end_dt.strftime("%Y-%m-%d")
                end_dt_for_log = end_dt

            room_id = random.choice(rooms)[0]
            grund = random.choice(GRUENDE_POOL)
            
            aufnahmen.append((a_id, p_id, start_dt.strftime("%Y-%m-%d"), end_str, grund))
            belegungen.append((bel_id, room_id, p_id, start_dt.strftime("%Y-%m-%d"), end_str))
            
            # Behandlungen innerhalb des Zeitraums
            for _ in range(random.randint(1, 3)):
                beh_date = start_dt + timedelta(days=random.randint(0, (end_dt_for_log - start_dt).days))
                behandlungen.append((beh_id, a_id, beh_date.strftime("%Y-%m-%d"), random.choice(TREATMENT_TEXTS)))
                b_aerzte.append((ba_rel_id, beh_id, random.choice(doctors)[0]))
                beh_id += 1; ba_rel_id += 1
            
            # Diagnose & Arzt
            pds.append((pd_id, a_id, random.choice(diagnoses)[0], start_dt.strftime("%Y-%m-%d"), random.choice(["NIEDRIG", "MITTEL", "HOCH"])))
            p_aerzte.append((pa_rel_id, pd_id, random.choice(doctors)[0]))
            
            # Betreuer zuordnen
            a_betreuer.append((ab_rel_id, a_id, random.choice(carers)[0]))
            
            a_id += 1; bel_id += 1; pd_id += 1; pa_rel_id += 1; ab_rel_id += 1

    # In Datenbank schreiben
    conn.executemany("INSERT INTO aufnahme VALUES (?, ?, ?, ?, ?)", aufnahmen)
    conn.executemany("INSERT INTO belegt VALUES (?, ?, ?, ?, ?)", belegungen)
    conn.executemany("INSERT INTO behandlung VALUES (?, ?, ?, ?)", behandlungen)
    conn.executemany("INSERT INTO behandlung_arzt VALUES (?, ?, ?)", b_aerzte)
    conn.executemany("INSERT INTO pd VALUES (?, ?, ?, ?, ?)", pds)
    conn.executemany("INSERT INTO pd_arzt VALUES (?, ?, ?)", p_aerzte)
    conn.executemany("INSERT INTO aufnahme_betreuer VALUES (?, ?, ?)", a_betreuer)

    conn.commit()
    
    # Statistik-Check
    active_count = conn.execute("SELECT COUNT(*) FROM aufnahme WHERE entlassungsdatum IS NULL").fetchone()[0]
    print(f"Datenbank erfolgreich erstellt.")
    print(f"Aktive Aufnahmen (Entlassungsdatum NULL): {active_count}")
    conn.close()

if __name__ == "__main__":
    main()