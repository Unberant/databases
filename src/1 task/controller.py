from model import Model
from view import View

from model import Airport, Aircraft, AirportAircraft, Ticket, UserAccount

class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()

    def menu(self):
        while True:
            try:
                self.view.menu()
                choice = int(input('Enter your choice: '))
                match choice:
                    case 1: # show all tablesList
                        for table in [Airport, Aircraft, AirportAircraft, Ticket, UserAccount]:
                            data = self.model.get_table_data(table)
                            self.view.show_table(table, data)
                    case 2: # show table
                        table = self.choose_table()
                        data = self.model.get_table_data(table)
                        self.view.show_table(table, data)
                    case 3: # add new record
                        table = self.choose_table()
                        self.view.show_table(table, self.model.get_table_data(table))
                        self.model.insert_into_table(table, self.enter_data_to_insert(table))
                        self.view.show_table(table, self.model.get_table_data(table))
                    case 4: # update record
                        table = self.choose_table()
                        self.view.show_table(table, self.model.get_table_data(table))
                        self.model.update_table(table, self.enter_data_to_update(table))
                        self.view.show_table(table, self.model.get_table_data(table))
                    case 5: # delete record
                        table = self.choose_table()
                        self.view.show_table(table, self.model.get_table_data(table))
                        self.model.delete_table(table, self.enter_data_to_delete(table))
                        self.view.show_table(table, self.model.get_table_data(table))
                    case 6: # add new random records
                        count = int(input('Enter count of records: '))
                        self.model.insert_random_data(count)
                        print('Done')
                    case 7: # exit
                        exit()
                    case _: print('Invalid choice, retry')
            except ValueError as err: print('Exception: ', err)

    def choose_table(self):
        self.view.list_of_tables()
        while True:
            try:
                choice = int(input('Enter your choice: '))
                match choice:
                    case 1: # Airport
                        return (Airport)
                    case 2: # Aircraft
                        return (Aircraft)
                    case 3: # airport_aircraft
                        return (AirportAircraft)
                    case 4: # Ticket
                        return (Ticket)
                    case 5: # User Account
                        return (UserAccount)
                    case 6: # exit
                        self.menu()
                        exit()
                    case _: print('Invalid choice, retry')
            except ValueError as err: print('Exception: ', err)

    def enter_data_to_insert(self, table) -> list[str]:
        print('\nEnter data for insert in table: ', table.__tablename__)
        data = []
        start_index = 1
        if table.__tablename__ == 'airport_aircraft':
            start_index = 0

        for column in table.columns[start_index:]:
            data.append(input('\tEnter ' + column + ': '))
        try:
            for key in table.addition_keys:
                data.append(input('\tEnter ' + key + ': '))
        except AttributeError: pass

        return data

    def enter_data_to_update(self, table):
        print('\nEnter data for update table: ', table.__tablename__)
        data = []

        for column in table.columns:
            data.append(input('\tEnter ' + column + ': '))
        return data

    def enter_data_to_delete(self, table):
        print('\nEnter data for delete from table: ', table.__tablename__)
        return input(f'\tEnter {table.columns[0]} for delete: ')

    def input_data_to_search(self):
        return input('\tEnter data to search: ')
