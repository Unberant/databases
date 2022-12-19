airport_table = [
    'airport_id',
    'name',
    'location'
]

aircraft_table = [
    'aircraft_id',
    'pilot',
    'name',
    'owner',
]

airport_aircraft_table = [
    'aircraft_id',
    'airport_id',
]

ticket_table = [
    'ticket_id',
    'price',
    'class',
    'date',
    'duration',
    'aircraft_id',
    'user_acc_id',
]

user_account_table = [
    'user_acc_id',
    'name',
    'mailbox',
    'bank_card',
]


class table:
    def __init__(self, name: str, columns: list, associated_keys: list = None,):
        self.name    = name
        self.columns = columns.copy()
        self.id      = columns[0]
        if name != 'airport_aircraft':
            columns.pop(0)
        self.changing_columns = columns
        self.associated_keys = None
        if associated_keys is not None:
            self.associated_keys = associated_keys.copy()

    def get_table_id(self):
        return self.columns[0]

    def get_all_columns(self):
        columns = self.changing_columns.copy()
        if self.associated_keys is not None:
            columns += self.associated_keys
        return columns

tablesList = [
    table('airport', airport_table),
    table('aircraft', aircraft_table, [airport_aircraft_table[1]]),
    table('airport_aircraft', airport_aircraft_table),
    table('ticket', ticket_table),
    table('user_account', user_account_table),
]
