from random import choice

import psycopg2
import psycopg2.extras

from tables import tablesList, table

class Model:
    def __init__(self):
        self.connection = psycopg2.connect(
            host ='localhost',
            user = "postgres",
            password = 'qwerty',
            database = 'airport',
        )
        self.connection.autocommit = True

    def select(self, table: table):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM \"{table.name}\" " +
                           f"ORDER BY \"{table.id}\" ASC")
            return cursor.fetchall()

    def insert_into_table(self, table: table, data: list):
        match table.name:
            case 'aircraft':
                airport_id = data.pop()
                self.insert_into(table, data) # insert into aircraft
                aircraft_id = self.select(table)[-1][0]
                self.insert_into(tablesList[2], [aircraft_id, airport_id]) # insert into airport_aircraft
            case _:
                self.insert_into(table, data)

    def insert_into(self, table: table, data):
        parsed_colms = ''
        for inserted_column in table.changing_columns:
            parsed_colms += f'{inserted_column}' + ', '
        parsed_colms = parsed_colms[:-2]
        inserted_data = ''
        for value in data:
            inserted_data += f'\'{value}\'' + ', '
        inserted_data = inserted_data[:-2]

        with self.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO \"{table.name}\" ({parsed_colms}) " +
                           f"VALUES({inserted_data});")

    def update_table(self, table: table, data):
        setter = "SET "
        columns = table.changing_columns
        id = data.pop(0)
        if len(columns) != len(data): raise Exception('Wrong data input')
        for i in range(0, len(columns)):
            setter += f'"{columns[i]}" = \'{data[i]}\', '
        setter = setter[:-2]

        with self.connection.cursor() as cursor:
            cursor.execute(f"UPDATE \"{table.name}\" " +
                           f"{setter} " +
                           f"WHERE \"{table.id}\" = {id};")

    def delete_table(self, table: table, data):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM \"{table.name}\" " +
                           f"WHERE {table.id} = {data[0]};")

    def search_in_table(self, table: table, data):
        searcher = "WHERE "
        for column in table.columns:
            searcher += f'\"{column}\"::text LIKE \'%{data}%\' OR '
        searcher = searcher[:-4]

        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM \"{table.name}\" " +
                           f"{searcher};")
            return cursor.fetchall()

    def insert_random_data(self, count: int):
        for i in range(0, count):
            with self.connection.cursor() as cursor:
                inserted_data = [
                    self.generate_random_str(),
                    self.generate_random_str(),
                ]
                self.insert_into_table(tablesList[0], inserted_data) # insert into airport

                inserted_data = [
                    self.generate_random_str(),
                    self.generate_random_str(),
                    self.generate_random_str(),
                    choice(self.get_ids_from_table(tablesList[0]))[0],
                ]
                self.insert_into_table(tablesList[1], inserted_data) # insert into aircraft

                inserted_data = [
                    choice(self.get_ids_from_table(tablesList[1]))[0],
                    choice(self.get_ids_from_table(tablesList[0]))[0],
                ]
                self.insert_into_table(tablesList[2], inserted_data) # insert into airport_aircraft

                inserted_data = [
                    self.generate_random_int(),
                    choice(['A', 'B', 'C', 'D', 'E']),
                    self.generate_random_time(),
                    self.generate_random_duration(),
                    choice(self.get_ids_from_table(tablesList[1]))[0],
                    choice(self.get_ids_from_table(tablesList[4]))[0],
                ]
                self.insert_into_table(tablesList[3], inserted_data) # insert into tiket

                inserted_data = [
                    self.generate_random_str(),
                    self.generate_random_str(),
                    self.generate_random_int(),
                ]
                self.insert_into_table(tablesList[4], inserted_data) # insert into user_account

    def generate_random_str(self):
        uppercase_letter = "chr(ascii('A') + (random() * 25)::int) "
        lowercase_letter = "chr(ascii('a') + (random() * 25)::int) "
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT ({uppercase_letter} || {lowercase_letter});")
            return cursor.fetchone()[0]

    def generate_random_int(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT trunc(random() * 1000)::int")
            return cursor.fetchone()[0]

    def generate_random_time(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT timestamp '2022-11-10 13:00:00'
                           + make_interval(days  => (random() * 30)::int)
                           + make_interval(hours => (random() * 45)::int)
                           + make_interval(mins  => (random() * 59)::int)
                           """)
            return cursor.fetchone()[0]

    def generate_random_duration(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT time '1:00:00' + make_interval(hours => (random() * 24)::int)")
            return cursor.fetchone()[0]

    def get_ids_from_table(self, table: table):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT \"{table.id}\" FROM \"{table.name}\";")
            return cursor.fetchall()
