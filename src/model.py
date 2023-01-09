import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import string
import random
import randomtimestamp
from typing import Any, List, Tuple

user = 'postgres'
password = 'qwerty'
host = 'localhost'
port = 5432
database = 'airport'


def get_engine():
    return create_engine(url=f"postgresql://{user}:{password}@{host}:{port}/{database}")

def connect():
    try:
        _engine = get_engine()
        Base.metadata.create_all(_engine)
        print(f"Connection to the {host} for user {user} created successfully.")
        return sessionmaker(bind=_engine)()
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

Base = declarative_base()

class Airport(Base):
    __tablename__  = 'airport'
    columns = ['airport_id','name','location']
    airport_id = Column(Integer, primary_key=True)
    name       = Column(String)
    location   = Column(String)

    def __init__(self, name, location):
        self.name = name
        self.location = location
        super(Airport, self).__init__()
    def id(self):
        return self.airport_id

class Aircraft(Base):
    __tablename__ = 'aircraft'
    columns       = ['aircraft_id','pilot','name','owner']
    addition_keys = ['airport_id']
    aircraft_id = Column(Integer, primary_key=True)
    pilot       = Column(String)
    name        = Column(String)
    owner       = Column(String)

    def __init__(self, pilot, name, owner):
        self.pilot = pilot
        self.name = name
        self.owner = owner
        super(Aircraft, self).__init__()
    def id(self):
        return self.aircraft_id

class AirportAircraft(Base):
    __tablename__ = 'airport_aircraft'
    columns = ['aircraft_id','airport_id']
    aircraft_id = Column(Integer, ForeignKey('aircraft.aircraft_id'), primary_key=True)
    airport_id  = Column(Integer, ForeignKey('airport.airport_id'), primary_key=True)

    def __init__(self, aircraft_id, airport_id):
        self.aircraft_id = aircraft_id
        self.airport_id = airport_id
        super(AirportAircraft, self).__init__()
    def id(self):
        return self.aircraft_id

class Ticket(Base):
    __tablename__ = 'ticket'
    columns = ['ticket_id','price','seat_type','date','duration','aircraft_id','user_acc_id']
    ticket_id    = Column(Integer, primary_key=True)
    price        = Column(Integer)
    seat_type    = Column(String)
    date         = Column(String)
    duration     = Column(Integer)
    aircraft_id  = Column(Integer, ForeignKey('aircraft.aircraft_id'))
    user_acc_id  = Column(Integer, ForeignKey('user_account.user_acc_id'))

    def __init__(self, price, seat_type, date, duration, aircraft_id, user_acc_id):
        self.price = price
        self.seat_type = seat_type
        self.date = date
        self.duration = duration
        self.aircraft_id = aircraft_id
        self.user_acc_id = user_acc_id
        super(Ticket, self).__init__()
    def id(self):
        return self.ticket_id


class UserAccount(Base):
    __tablename__ = 'user_account'
    columns = ['user_acc_id','name','mailbox','bank_card']
    user_acc_id = Column(Integer, primary_key=True)
    name        = Column(String)
    mailbox     = Column(String)
    bank_card   = Column(String)

    def __init__(self, name, mailbox, bank_card):
        self.name = name
        self.mailbox = mailbox
        self.bank_card = bank_card
        super(UserAccount, self).__init__()
    def id(self):
        return self.user_acc_id


class Model:
    def __init__(self):
        self.session = connect()

    def get_table_data(self, table) -> List[Tuple[Any]]:
        return [tuple(getattr(item, col.name) for col in item.__table__.columns)
            for item in self.session.query(table).order_by(table.id(table).asc()).all()]

    def insert_into_table(self, table, data: list[str]):
        try:
            match table.__tablename__:
                case 'aircraft':
                    airport_id = data.pop()
                    self.session.add(table(*data)) # insert into aircraft
                    self.session.commit()
                    aircraft_id = self.session.query(Aircraft).order_by(Aircraft.aircraft_id.desc()).first().aircraft_id
                    self.session.add(AirportAircraft(aircraft_id, airport_id)) # insert into airport_aircraft
                case _:
                    self.session.add(table(*data))
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_table(self, table, data):
        try:
            row = self.session.query(table).filter(table.id(table) == int(data[0])).first()
            columns = [col for col in row.__table__.columns.keys()]
            for column, value in zip(columns, data):
                row.__setattr__(column, value)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def delete_table(self, table, id):
        try:
            row = self.session.query(table).filter(table.id(table) == int(id)).first()
            if row: self.session.delete(row)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def insert_random_data(self, count: int):
        for i in range(0, count):
            inserted_data = [
                self.generate_random_str(),
                self.generate_random_str(),
            ]
            self.insert_into_table(Airport, inserted_data) # insert into airport

            inserted_data = [
                self.generate_random_str(),
                self.generate_random_str(),
                self.generate_random_str(),
                self.get_random_id_from_table(Airport),
            ]
            self.insert_into_table(Aircraft, inserted_data) # insert into aircraft

            inserted_data = [
                self.get_random_id_from_table(Aircraft),
                self.get_random_id_from_table(Airport),
            ]
            self.insert_into_table(AirportAircraft, inserted_data) # insert into airport_aircraft

            inserted_data = [
                self.generate_random_int(),
                random.choice(['A', 'B', 'C', 'D', 'E']),
                self.generate_random_time(),
                self.generate_random_duration(),
                self.get_random_id_from_table(Aircraft),
                self.get_random_id_from_table(UserAccount),
            ]
            self.insert_into_table(Ticket, inserted_data) # insert into tiket

            inserted_data = [
                self.generate_random_str(),
                self.generate_random_str(),
                self.generate_random_int(),
            ]
            self.insert_into_table(UserAccount, inserted_data) # insert into user_account

    def generate_random_str(self):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(10))

    def generate_random_int(self):
        return str(random.randint(10, 5000))

    def generate_random_time(self):
        return str(randomtimestamp.randomtimestamp(pattern='%Y-%m-%d %H:%M:%S'))

    def generate_random_duration(self):
        return str(randomtimestamp.random_time())

    def get_random_id_from_table(self, table):
        data = self.get_table_data(table)
        row = int(random.randint(0, len(data) - 1))
        return data[row][0]

