import csv
import re
import os
import traceback
import datetime
import sys


def extract_lineup(row):
    # Create dictionary of CSV row values
    # Extracts the ID for each URL
    lineup_dict = {'band_url': row[0].replace('\ufeff', ''),
                   'band_id': extract_id(row[0]),
                   'album_url': row[1],
                   'album_id': extract_id(row[1]),
                   'artist_name': row[2],
                   'artist_url': row[3],
                   'artist_id': extract_id(row[3]),
                   'roles': row[4],
                   'lineup_type': row[5],
                   'lineup_version': row[6],
                   'scrape_datetime': row[7]}

    return lineup_dict


def extract_id(URL):
    """
    Searches for the digits at the end of a URL which is the ID.
    It will not find the ID if there is no URL.

    Args:
        URL (string): URL to extract the ID from

    Returns:
        string: ID extracted from URL, or if there is no URL, an empty string
    """
    id_search = re.search(r'\d*$', URL)
    if id_search is None:
        return ''
    else:
        return id_search.group()


def extract_role_parenthesis(role_dict):
    split_role_parenthesis(role_dict)

    for r in role_dict['roles']:
        if extract_track_parenthesis(role_dict, r):
            role_dict['role_sub'] = re.split(r',', r)
            for sub in role_dict['role_sub']:
                extract_solo_parenthesis(role_dict, sub)
                extract_additional_parenthesis(role_dict, sub)
                extract_attribution_parenthesis(role_dict, sub)

        role_dict['role_sub'] = list(map(str.strip, role_dict['role_sub']))
        role_dict['role_sub'] = list(map(str.title, role_dict['role_sub']))


def split_role_parenthesis(role_dict):
    role_split_list = re.split(r'\(|\[| on (?=track)',
                               re.sub(r'\)|\]', '', role_dict['roles']))

    role_dict['role'] = role_split_list.pop(0).title()
    if 'solo' in role_dict['role'].lower():
        role_dict['solo'] = True
        role_dict['role'] = re.sub(r' [Ss]oloS?', '', role_dict['role'])

    role_dict['roles'] = role_split_list


def extract_track_parenthesis(role_dict, r):
    role_tracks_search = re.search(r'[Tt]racks? ([\d,\-&\s(and)]+)', r)
    if role_tracks_search is not None:
        role_except_search = re.search(
            r'[Ee]xcept ?[Oo]?n? [Tt]racks? ([\d,\-&\s(and)]+)', r)

        role_tracks = role_tracks_search.group(1)
        role_tracks_list = re.split(r',|\sand|&', role_tracks)

        # Check if there are any track ranges and expand them
        pop_list = []
        for t in range(len(role_tracks_list)):
            if '-' in role_tracks_list[t]:
                pop_list.append(t)
                track_range_split = re.split('-', role_tracks_list[t])
                role_tracks_list.extend(list(map(str,
                                                 range(int(track_range_split
                                                           [0]),
                                                       int(track_range_split
                                                           [1]) + 1))))

        role_tracks_list = [v for i, v in enumerate(role_tracks_list)
                            if i not in pop_list]
        role_tracks_list = list(map(str.strip, role_tracks_list))
        role_tracks_list = sorted(list(map(int, role_tracks_list)))
        role_dict['tracks'] = list(map(str, role_tracks_list))

        if role_except_search is not None:
            role_dict['except'] = True

        return False
    else:
        return True


def extract_solo_parenthesis(role_dict, sub):
    # Extracts solo reference from the element
    # Also removes the element from the list
    if 'solo' in sub.lower():
        role_dict['solo'] = True
        role_dict['role_sub'].remove(sub)


def extract_additional_parenthesis(role_dict, sub):
    # Extracts additional reference from the element
    # Also removes the element from the list
    if 'additional' in sub.lower():
        role_dict['additional'] = True
        role_dict['role_sub'].remove(sub)


def extract_attribution_parenthesis(role_dict, sub):
    attribution_search = re.search(r'as "?(.*?)"?', sub)
    if attribution_search is not None:
        role_dict['attribution'] = attribution_search.group(1)
        role_dict['role_sub'].remove(sub)


def extract_role_no_parenthesis(role_dict):

    extract_track_no_parenthesis(role_dict)
    extract_solo_no_parenthesis(role_dict)
    extract_additional_no_parenthesis(role_dict)

    role_dict['role'] = role_dict['roles'].title()


def extract_track_no_parenthesis(role_dict):
    role_tracks_search = re.search(
        r'[Tt]racks? ([\d,\-&\s(and)]+)', role_dict['roles'])
    if role_tracks_search is not None:
        role_except_search = re.search(
            r'[Ee]xcept ?[Oo]?n? [Tt]racks? ([\d,\s]+)', role_dict['roles'])

        role_tracks = role_tracks_search.group(1)
        role_tracks_list = re.split(r',|\sand|&', role_tracks)

        # Check if there are any track ranges and expand them
        pop_list = []
        for t in range(len(role_tracks_list)):
            if '-' in role_tracks_list[t]:
                pop_list.append(t)
                track_range_split = re.split('-', role_tracks_list[t])
                role_tracks_list.extend(list(map(str,
                                                 range(int(track_range_split
                                                           [0]),
                                                       int(track_range_split
                                                           [1]) + 1))))

        # Remove the
        role_tracks_list = [v for i, v in enumerate(role_tracks_list)
                            if i not in pop_list]

        # String leading and trailing spaces
        # Convert list to integers and sort
        # Convert list to strings
        role_tracks_list = list(map(str.strip, role_tracks_list))
        role_tracks_list = sorted(list(map(int, role_tracks_list)))
        role_dict['tracks'] = list(map(str, role_tracks_list))
        role = re.sub(r'[Oo]?n? [Tt]racks? [\d,\-&\s(and)]+', '',
                      role_dict['roles'])

        if role_except_search is not None:
            role_dict['except'] = True
            role = re.sub('[Ee]xcept', '', role_dict['roles'])

        role_dict['roles'] = role.strip()


def extract_solo_no_parenthesis(role_dict):
    # Extracts solo reference from the element
    # Also removes "solo" from the string
    if 'solo' in role_dict['roles'].lower():
        role_dict['solo'] = True
        role_dict['roles'] = re.sub(r' [Ss]olo', '', role_dict['roles'])


def extract_additional_no_parenthesis(role_dict):
    # Extracts additional reference from the element
    # Also removes "additional" from the string
    if 'additional' in role_dict['roles'].lower():
        role_dict['additional'] = True
        role_dict['roles'] = re.sub(
            r'^[Aa]dditional | [Aa]dditional', '', role_dict['roles'])


def create_csv():
    # Create or overwrite CSV file to save data in
    if os.path.isfile(r'data\transformed\album-lineup-transformed.csv'):
        os.remove(r'data\transformed\album-lineup-transformed.csv')

    with open(r'data\transformed\album-lineup-transformed.csv', 'w', newline='',
              encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar=r'"')
        csv_writer.writerow(['band_url',
                             'band_id',
                             'album_url',
                             'album_id',
                             'artist_name',
                             'artist_url',
                             'artist_id',
                             'roles',
                             'lineup_type',
                             'lineup_version',
                             'role',
                             'role_sub',
                             'additional',
                             'solo',
                             'attribution',
                             'tracks',
                             'except_tracks',
                             'scrape_datetime',
                             'transform_datetime'])


def create_csv_error():
    # Create or overwrite CSV file to save data in
    if os.path.isfile(r'data\transformed\album-lineup-transformed-error.csv'):
        os.remove(r'data\transformed\album-lineup-transformed-error.csv')

    with open(r'data\transformed\album-lineup-transformed-error.csv', 'w',
              newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar=r'"')
        csv_writer.writerow(['band_url',
                             'band_id',
                             'album_url',
                             'album_id',
                             'artist_name',
                             'artist_url',
                             'artist_id',
                             'roles',
                             'lineup_type',
                             'lineup_version',
                             'csv_row',
                             'exception'])


def write_to_csv(lineup_dict, role_dict):
    # Append rows for each role subtype for the role
    # If there is no subtype it will just append the one row for the role
    with open(r'data\transformed\album-lineup-transformed.csv', 'a+', newline='',
              encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar=r'"')

        if len(role_dict['role_sub']) > 0:
            for sub in role_dict['role_sub']:
                csv_writer.writerow([lineup_dict['band_url'],
                                     lineup_dict['band_id'],
                                     lineup_dict['album_url'],
                                     lineup_dict['album_id'],
                                     lineup_dict['artist_name'],
                                     lineup_dict['artist_url'],
                                     lineup_dict['artist_id'],
                                     lineup_dict['roles'],
                                     lineup_dict['lineup_type'],
                                     lineup_dict['lineup_version'],
                                     role_dict['role'],
                                     sub,
                                     role_dict['additional'],
                                     role_dict['solo'],
                                     role_dict['attribution'],
                                     ','.join(role_dict['tracks']),
                                     role_dict['except_tracks'],
                                     lineup_dict['scrape_datetime'] + ':00',
                                     datetime.datetime.now().strftime('%d/%m/%Y '
                                                                      r'%H:%M:%S')])
        else:
            csv_writer.writerow([lineup_dict['band_url'],
                                 lineup_dict['band_id'],
                                 lineup_dict['album_url'],
                                 lineup_dict['album_id'],
                                 lineup_dict['artist_name'],
                                 lineup_dict['artist_url'],
                                 lineup_dict['artist_id'],
                                 lineup_dict['roles'],
                                 lineup_dict['lineup_type'],
                                 lineup_dict['lineup_version'],
                                 role_dict['role'],
                                 '',
                                 role_dict['additional'],
                                 role_dict['solo'],
                                 role_dict['attribution'],
                                 ','.join(role_dict['tracks']),
                                 role_dict['except_tracks'],
                                 lineup_dict['scrape_datetime'] + ':00',
                                 datetime.datetime.now().strftime(r'%d/%m/%Y '
                                                                  r'%H:%M:%S')])


def write_to_csv_error(lineup_dict, role_dict, csv_row, e):
    # If there is an exception this will add a row with no role data
    # Also writes the exception
    with open(r'data\transformed\album-lineup-transformed-error.csv', 'a+',
              newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar=r'"')

        csv_writer.writerow([lineup_dict['band_url'],
                             lineup_dict['band_id'],
                             lineup_dict['album_url'],
                             lineup_dict['album_id'],
                             lineup_dict['artist_name'],
                             lineup_dict['artist_url'],
                             lineup_dict['artist_id'],
                             lineup_dict['roles'],
                             lineup_dict['lineup_type'],
                             lineup_dict['lineup_version'],
                             str(csv_row),
                             str(traceback.format_exception(e))])


def main():
    csv_row = 0

    create_csv()
    create_csv_error()

    with open(r'data\raw\album-lineup.csv', 'r', newline='',
              encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar=r'"')
        for row in csv_reader:
            lineup_dict = extract_lineup(row)
            roles_split = re.split(r',\s?(?![^()]*\)|\d)',
                                   lineup_dict['roles'])

            print('')
            print(csv_row := csv_row + 1)
            print(roles_split)

            for role in roles_split:
                role_dict = {'roles': role,
                             'role': '',
                             'role_sub': [],
                             'additional': False,
                             'solo': False,
                             'attribution': '',
                             'tracks': [],
                             'except_tracks': False}

                # Split
                try:
                    if '(' in role or '[' in role:
                        extract_role_parenthesis(role_dict)

                    else:
                        extract_role_no_parenthesis(role_dict)
                    role_dict.pop("roles")

                    print(role_dict)

                    write_to_csv(lineup_dict, role_dict)
                except Exception as e:
                    write_to_csv_error(lineup_dict, role_dict,
                                       csv_row, e)


if __name__ == "__main__":
    main()
