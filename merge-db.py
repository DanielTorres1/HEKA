#!/usr/bin/python3
import sqlite3
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Consolidate data for a specific country.')
parser.add_argument('country', type=str, help='The name of the country to consolidate data for.')
  
args = parser.parse_args()

# Call the function with the provided arguments
country=args.country
    
destination_folder = "consolidado"

# # Define the source folders
#source_folders = [f'{country}1', f'{country}2', f'{country}3', f'{country}4', f'{country}5']
source_folders = [f'{country}1', f'{country}2', f'{country}3', f'{country}4']

# # Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

 # Copy the contents of each source folder to the destination folder
print ("COPIANDO ARCHIVOS")
for folder in source_folders:
    if os.path.isdir(folder):
        for item in os.listdir(folder):
            source_path = os.path.join(folder, item)
            destination_path = os.path.join(destination_folder, item)
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            else:
                shutil.copy2(source_path, destination_path)



print ("UNIEDO BDs")
# List of database filenames
#db_files = [f'{country}1/.resultados.db', f'{country}2/.resultados.db', f'{country}3/.resultados.db', f'{country}4/.resultados.db', f'{country}5/.resultados.db']
db_files = [f'{country}1/.resultados.db', f'{country}2/.resultados.db', f'{country}3/.resultados.db', f'{country}4/.resultados.db']


#delete old DB
os.remove('consolidado/.resultados.db')

# Connect to the new merged database
conn = sqlite3.connect('consolidado/.resultados.db')
cursor = conn.cursor()

# Create tables in the new database
cursor.executescript('''
CREATE TABLE IF NOT EXISTS BANNERS (
    IP CHAR(30),
    PUERTO INT,
    ENUM TEXT
);

CREATE TABLE IF NOT EXISTS ENUMERACION (
    IP CHAR(30),
    PUERTO INT,
    TIPO CHAR(30),
    ENUM TEXT
);

CREATE TABLE IF NOT EXISTS VULNERABILIDADES (
    IP CHAR(30),
    PORT CHAR(30),
    TIPO CHAR(30),
    VULN CHAR(50)
);

CREATE TABLE IF NOT EXISTS SERVICIOSWEB (
    URL TEXT,
    TITLE TEXT
);

CREATE TABLE IF NOT EXISTS PANELESADMIN (
    URL TEXT,
    TITLE TEXT,
    DESCRIPCION TEXT
);
''')

# Attach databases and merge data
for db_file in db_files:
    cursor.execute(f"ATTACH DATABASE '{db_file}' AS db")
    cursor.executescript('''
    INSERT INTO BANNERS SELECT * FROM db.BANNERS;
    INSERT INTO ENUMERACION SELECT * FROM db.ENUMERACION;
    INSERT INTO VULNERABILIDADES SELECT * FROM db.VULNERABILIDADES;
    INSERT INTO SERVICIOSWEB SELECT * FROM db.SERVICIOSWEB;
    INSERT INTO PANELESADMIN SELECT * FROM db.PANELESADMIN;
    ''')
    cursor.execute("DETACH DATABASE db")

# Commit changes and close the connection
conn.commit()
conn.close()
