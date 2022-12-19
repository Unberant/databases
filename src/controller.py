from model import Model
from view import View
from datetime import datetime

from tables import tablesList, table

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
                        for i in range(0, len(tablesList)):
                            data = self.model.select(tablesList[i])
                            self.view.show_table(tablesList[i], data)
                    case 2: # show table
                        table = self.choose_table()
                        data = self.model.select(table)
                        self.view.show_table(table, data)
                    case 3: # add new record
                        table = self.choose_table()
                        self.view.show_table(table, self.model.select(table))
                        self.model.insert_into_table(table, self.input_data(table, 'insert'))
                        self.view.show_table(table, self.model.select(table))
                    case 4: # update record
                        table = self.choose_table()
                        self.view.show_table(table, self.model.select(table))
                        self.model.update_table(table, self.input_data(table, 'update'))
                        self.view.show_table(table, self.model.select(table))
                    case 5: # delete record
                        table = self.choose_table()
                        self.view.show_table(table, self.model.select(table))
                        self.model.delete_table(table, self.input_data(table, 'delete'))
                        self.view.show_table(table, self.model.select(table))
                    case 6: # add new random records
                        count = int(input('Enter count of records: '))
                        self.model.insert_random_data(count)
                        print('Done')
                    case 7: # search
                        table  = self.choose_table()
                        result = self.model.search_in_table(table, input('\tEnter data to search: '))
                        self.view.show_table(table, result)
                    case 8: # exit
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
                        return (tablesList[0])
                    case 2: # Aircraft
                        return (tablesList[1])
                    case 3: # airport_aircraft
                        return (tablesList[2])
                    case 4: # Ticket
                        return (tablesList[3])
                    case 5: # User Account
                        return (tablesList[4])
                    case 6: # exit
                        self.menu()
                        exit()
                    case _: print('Invalid choice, retry')
            except ValueError as err: print('Exception: ', err)

    def input_data(self, table: table, instruction):
        data = []
        print('\nEnter data for table: ', table.name)
        print(" ! You can set up default value for field just by typing 'def'")
        print(" ! Disabled for Primary&Foreign keys")
        columns = []
        index = 0
        match instruction:
            case 'insert':
                columns = table.get_all_columns()
            case 'update':
                index = 1
                columns = table.columns
            case 'delete':
                index = 1
                columns = [table.columns[0]]

        if instruction == 'update' and table.name == 'airport_aircraft':
            data.append(input('\tEnter current aircraft_id: '))
        for column in columns:
            data.append(input('\tEnter ' + column + ': '))

        if instruction == 'delete': return data
        match table.name:
            case 'airport': # Airport
                if data[index] == 'def': data[index] = 'London City Airport'
                index += 1
                if data[index] == 'def': data[index] = 'Newham, London, UK'
            case 'aircraft': # Aircraft
                if data[index] == 'def': data[index] = 'Andrew Russel'
                index += 1
                if data[index] == 'def': data[index] = 'Boeing 737-800'
                index += 1
                if data[index] == 'def': data[index] = 'Airbuss'
                index += 1
                if instruction == 'insert' and data[index] == 'def':
                    print('Please retry input data, for this coloumn default option is disabled')
                    return self.input_data(table)
            case 'airport_aircraft': # airport_aircraft
                if data[0] == 'def' or data[1] == 'def':
                    print('Please retry input data, for this table default option is disabled')
                    return self.input_data(table)
            case 'ticket': # Ticket
                if data[index] == 'def': data[index] = '1000'
                index += 1
                if data[index] == 'def': data[index] = 'E'
                index += 1
                if data[index] == 'def': data[index] = '2022-10-10 ' + datetime.now().strftime("%H:%M:%S")
                index += 1
                if data[index] == 'def': data[index] = '05:00:00'
                index += 1
                if data[index] == 'def' or data[index+1] == 'def':
                    print('Please retry input data, for foreign keys default option is disabled')
                    return self.input_data(table)
            case 'user_account': # User Account
                if data[index] == 'def': data[index] = 'admin'
                index += 1
                if data[index] == 'def': data[index] = 'admin@mainbox.com'
                index += 1
                if data[index] == 'def': data[index] = '0000000000000000'
            case _: 
                print('Invalid choice, retry')
                return self.input_data(table)
        return data

    def input_data_to_search(self):
        return input('\tEnter data to search: ')
