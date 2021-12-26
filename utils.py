import pyodbc
import pandas as pd


class Connection:
    """
    Classe de conexão ao banco de dados do cartola. Originalmente é um banco de dados local.
    """
    def __init__(self):
        server = r'DESKTOP-EKCEMPT\SQLEXPRESS'
        database = 'CSGO_STATS'
        username = 'mauroban'
        password = 'cartola123'

        self.conexao = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                      'SERVER=' + server + ';'
                                      'DATABASE=' + database + ';'
                                      'UID=' + username + ';'
                                      'PWD=' + password)


def insert_to_database(df):
    if list(df.columns) == ['lineno', 'time', 'moment', 'mapnumber', 'round', 'map_name', 'match_id', 'type',
                            'author_name', 'author_id', 'author_side', 'victim_id', 'victim_name', 'victim_side',
                            'weapon', 'damage', 'blinded_time', 'flashbang_id', 'damage_armor', 'victim_health',
                            'victim_armor', 'hitgroup', 'hs', 'penetrated', 'throughsmoke', 'author_coord',
                            'victim_coord', 'equipment', 'item_bought', 'equipment_value']:

        df = df[df['moment'].isin(['live', 'freeze_time'])]

        df.dropna(subset=['time', 'type'], inplace=True)
        df['time'] = pd.to_datetime(df['time'], format=r'%m/%d/%Y - %H:%M:%S', errors='coerce')

        # df.fillna(value={'type': 'undefined'}, inplace=True)

        df = df.where(df.notnull(), None)

        print(df.info())

        insert_sql = """
        INSERT INTO [ALL_EVENTS]
                   ([lineno]
                   ,[time]
                   ,[moment]
                   ,[mapnumber]
                   ,[round]
                   ,[map_name]
                   ,[match_id]
                   ,[type]
                   ,[author_name]
                   ,[author_id]
                   ,[author_side]
                   ,[victim_id]
                   ,[victim_name]
                   ,[victim_side]
                   ,[weapon]
                   ,[damage]
                   ,[blinded_time]
                   ,[flashbang_id]
                   ,[damage_armor]
                   ,[victim_health]
                   ,[victim_armor]
                   ,[hitgroup]
                   ,[hs]
                   ,[penetrated]
                   ,[throughsmoke]
                   ,[author_coord]
                   ,[victim_coord]
                   ,[equipment]
                   ,[item_bought]
                   ,[equipment_value])
             VALUES
                   ( ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?
                   , ?)
        """

        cnx = Connection().conexao
        cursor = cnx.cursor()

        for row in df.values:
            print(list(row))
            row[25] = str(row[25])
            row[26] = str(row[26])
            cursor.execute(insert_sql, list(row))

        cursor.commit()
