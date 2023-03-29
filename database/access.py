# https://pythoninoffice.com/python-ms-access-database-pyodbc/
# https://datatofish.com/import-csv-sql-server-python/

import pyodbc
import pandas as pd
import insert_data


def display_tables():
    global cursor
    for i in cursor.tables(tableType='TABLE'):
        print(i.table_name)


def delete_data(cursor):
    cursor.execute('DELETE FROM album_lineup_cleaned')


def create_dataframe():
    df = pd.read_csv(r'data\transformed\album-lineup-transformed.csv',
                     na_filter=False)
    return pd.DataFrame(df)


def main():
    global cursor
    conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=C:\Users\Benjamin\OneDrive\03. Hobbies\09. Data'
                r'\Datagraphica Metallum\Python\datagraphica-metallum'
                r'\database\test.accdb;')
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    df = create_dataframe()
    delete_data(cursor)
    insert_data.album_lineup_cleaned(cursor, df)
    conn.commit()


if __name__ == "__main__":
    main()
