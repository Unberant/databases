class View:
    def __init__(self):
        self.table = None

    def menu(self):
        print('''
        Select an option:
            1. Show all tables
            2. Show table
            3. Add new record
            4. Update record
            5. Delete record
            6. Add new random records
            7. Exit
        ''')

    def list_of_tables(self):
        print('''
        Select a table:
            1. Airport
            2. Aircraft
            3. Airport/Aircraft
            4. Ticket
            5. Users Account
            6. Exit
        ''')

    def show_table(self, table, data):
        columns = table.columns
        column_width   = int(130 / len(columns))
        executor_width = 4
        print("\n" + f'  {table.__tablename__}  '.center(130 + executor_width, "="), end='\n    ')
        for column in columns:
            print(str(column).center(column_width," "), end='')
        print()
        for i, item in enumerate(data, start = 1):
            print(str(f'{i}.').center(executor_width," "), end='')
            for j in item:
                print(str(j).center(column_width, " "), end='')
            print()



