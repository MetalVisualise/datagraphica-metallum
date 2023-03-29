import re
import datetime


def insert_data(cursor, table_name, columns, data):
    # Use * as an unpacking operator to add list items as positional parameters
    value_ques = ','.join(['?']*len(columns))
    cursor.execute('INSERT INTO ' +
                   table_name +
                   ' (' +
                   ','.join(columns) +
                   '''
                   )

                   VALUES (
                   ''' +
                   value_ques +
                   ')',
                   *data
                   )


def album_lineup_transformed(cursor, df):
    table_name = 'album_lineup_transformed'
    columns = df.columns

    for index, row in df.iterrows():
        data = []
        for col in columns:
            value = row[col]
            datetime_match = re.search(r'\d{2}\/\d{2}\/\d{4}',
                                       str(value))
            if isinstance(value, bool):
                data.append('True' if bool(value) else 'False')
            elif datetime_match is not None:
                data.append(datetime.datetime.strptime(value,
                                                       '%d/%m/%Y %H:%M:%S'))
            else:
                data.append(str(value))

        insert_data(cursor, table_name, columns, data)
