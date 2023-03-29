# https://www.postgresql.org/docs/

import pyodbc
import pandas as pd
import insert_data
import create_table


def create_dataframe():
    df = pd.read_csv(r'data\transformed\album-lineup-transformed.csv',
                     na_filter=False)
    return pd.DataFrame(df)


def main():
    conn_str = (r'DRIVER={PostgreSQL Unicode};'
                r'UID=postgre;Password=password;Server=192.168.0.112;'
                r'Port=5432;Database=datagraphica_metallum;')
    conn = pyodbc.connect(conn_str)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')
    conn.maxwrite = 1024 * 1024 * 1024
    cursor = conn.cursor()

    df = create_dataframe()
    create_table.album_lineup_transformed(cursor, True)
    insert_data.album_lineup_transformed(cursor, df)
    conn.commit()


if __name__ == "__main__":
    main()
