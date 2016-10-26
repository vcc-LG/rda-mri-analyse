#Script to load in Siemens .rda files, save to database and do some pretty display/processing

import os, datetime
import subprocess
import sqlite3


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def create_database(database_path):
    conn = create_connection(database_path)
    f = open('sql\\sql_create_table.sql', 'r')
    sql = f.read()
    if conn is not None:
        create_table(conn, sql)
    else:
        print("Error! cannot create the database connection.")

def insert_into_database(database_path,my_file_name_strip,raw_data,time_stamp):
    conn = create_connection(database_path)
    f = open('sql\\sql_insert_data.sql', 'r')
    sql = f.read()
    place_holders = '?,'*(len(raw_data)+2)
    place_holders = place_holders[:-1]
    conc_data = []

    for row in raw_data:
        try:
            conc_data.append(float(row.split()[1]))
        except:
            conc_data.append('NULL')
    insert_data = [my_file_name_strip] + [time_stamp] + conc_data
    insert_sql = sql+place_holders+")"
    try:
        c = conn.cursor()
        c.execute(insert_sql,insert_data)
    except sqlite3.Error as e:
        print(e)

def get_tarquin_data(output_txt_path):
    with open(output_txt_path, "r") as ins:
        all_data = []
        for line in ins:
            if '--------' in line:
                break
        for line in ins:
            if not line.strip():
                break
            all_data.append(line)
    return all_data

def call_tarquin(input_path,my_file_name,my_output_path,database_path):
    my_file_name_strip = my_file_name.strip('.rda')
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    time_stamp_dir = time_stamp
    time_stamp_dir = time_stamp_dir.replace(' ','_')
    time_stamp_dir = time_stamp_dir.replace(':','')

    output_dir = os.path.join('output\\',my_file_name_strip+'_'+time_stamp_dir)
    os.makedirs(output_dir,
                exist_ok=True)
    output_txt_path = os.path.join(output_dir,my_file_name_strip+'.txt')
    tarquin_cmd = [r'tarquin\\tarquin\\tarquin.exe',
                   '--input',
                   input_file_path + file_name,
                   '--format','rda',
                   '--output_txt',
                   output_txt_path]
    subprocess.call(tarquin_cmd)
    raw_data = get_tarquin_data(output_txt_path)
    insert_into_database(database_path,my_file_name_strip,raw_data,time_stamp)

input_file_path = r'data\\'
output_file_path = r'output\\'
database_file_path = r'database\\'
database_file_name = 'rda_database2.db'
database_full_path = os.path.join(database_file_path,database_file_name)
create_database(database_full_path)

for file_name in os.listdir(input_file_path):
    call_tarquin(input_file_path,file_name,output_file_path,database_full_path)