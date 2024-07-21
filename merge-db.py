#!/usr/bin/python3
import sqlite3
import os
import shutil
import argparse
import re

parser = argparse.ArgumentParser(description='Consolidate data for a specific country.')
parser.add_argument('country', type=str, help='The name of the country to consolidate data for.')
args = parser.parse_args()

def get_source_folders(country):
    # Get the current working directory
    directory = os.getcwd()
    
    # Create a regex pattern to match folders like bolivia1, bolivia2, etc.
    pattern = re.compile(rf'{country}\d+')

    # List all items in the directory
    all_items = os.listdir(directory)

    # Filter the items that match the pattern and are directories
    source_folders = [item for item in all_items if pattern.match(item) and os.path.isdir(os.path.join(directory, item))]

    return source_folders

def get_db_files(country):
    # Get the current working directory
    directory = os.getcwd()
    
    # Create a regex pattern to match folders like bolivia1, bolivia2, etc.
    pattern = re.compile(rf'{country}\d+')

    # List all items in the directory
    all_items = os.listdir(directory)

    # Filter the items that match the pattern and are directories
    source_folders = [item for item in all_items if pattern.match(item) and os.path.isdir(os.path.join(directory, item))]

    # Create the list of .resultados.db files for each source folder
    db_files = [os.path.join(folder, '.resultados.db') for folder in source_folders]

    return db_files

# Call the function with the provided arguments
country=args.country
    
destination_folder = "consolidado"


# # Define the source folders
source_folders = get_source_folders(country)

# # Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Create the 'servicios_archived' folder in the destination
os.makedirs(os.path.join(destination_folder, 'servicios_archived'), exist_ok=True)


print("COPIANDO ARCHIVOS")
# Copy and append files from 'servicios_archived'
for folder in source_folders:
    source_servicios_archived = os.path.join(folder, 'servicios_archived')
    if os.path.isdir(source_servicios_archived):
        for item in os.listdir(source_servicios_archived):
            source_path = os.path.join(source_servicios_archived, item)
            destination_path = os.path.join(destination_folder, 'servicios_archived', item)
            
            try:
                if os.path.isdir(source_path):
                    if not os.path.exists(destination_path):
                        shutil.copytree(source_path, destination_path)
                    else:
                        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                else:
                    if os.path.exists(destination_path):
                        with open(source_path, 'rb') as src_file:
                            with open(destination_path, 'ab') as dest_file:
                                shutil.copyfileobj(src_file, dest_file)
                    else:
                        shutil.copy2(source_path, destination_path)
            except FileNotFoundError as e:
                print(f"Archivo no encontrado: {e}")
            except Exception as e:
                print(f"Error al copiar archivo {source_path}: {e}")

# Copy files from 'logs'
for folder in source_folders:
    source_logs = os.path.join(folder, 'logs')
    if os.path.isdir(source_logs):
        for item in os.listdir(source_logs):
            source_path = os.path.join(source_logs, item)
            destination_path = os.path.join(destination_folder, 'logs', item)
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

print("ARCHIVOS COPIADOS Y APENDIDOS CON ÉXITO")

print ("UNIEDO BDs")
# List of database filenames
#db_files = [f'{country}1/.resultados.db', f'{country}2/.resultados.db', f'{country}3/.resultados.db', f'{country}4/.resultados.db']
db_files = get_db_files(country)

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
