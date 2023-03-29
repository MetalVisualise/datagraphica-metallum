def create_table(cursor, table_name, columns_dict, drop):
    if drop:
        cursor.execute('DROP TABLE ' + table_name)

    cursor.execute('CREATE TABLE ' +
                   table_name +
                   ' (' +
                   ','.join([column + ' ' + type for column, type in
                             columns_dict.items()]) +
                   ')')


def album_lineup_transformed(cursor, drop):
    table_name = 'album_lineup_transformed'
    columns_dict = {'band_url': 'varchar',
                    'band_id': 'varchar',
                    'album_url': 'varchar',
                    'album_id': 'varchar',
                    'artist_name': 'varchar',
                    'artist_url': 'varchar',
                    'artist_id': 'varchar',
                    'roles': 'varchar',
                    'lineup_type': 'varchar',
                    'lineup_version': 'varchar',
                    'role': 'varchar',
                    'role_sub': 'varchar',
                    'additional': 'boolean',
                    'solo': 'boolean',
                    'attribution': 'varchar',
                    'tracks': 'varchar',
                    'except_tracks': 'boolean',
                    'scrape_datetime': 'timestamp',
                    'transform_datetime': 'timestamp'}
    create_table(cursor, table_name, columns_dict, drop)
