from base64 import b64encode
from random import randbytes, randint
from sqlite3 import connect
from uuid import uuid4

all_uuid = []


def gen_str(_len: int) -> str:
    c_uuid = b64encode(randbytes(_len)).decode()
    all_uuid.append(c_uuid)
    return c_uuid


db = connect('страховая_компания.db')
db.executescript('''
CREATE TABLE IF NOT EXISTS клиенты (
    айди UUID PRIMARY KEY NOT NULL,
    имя TEXT NOT NULL,
    фамилия TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS виды_страховок (
    айди INTEGER PRIMARY KEY AUTOINCREMENT,
    наименование TEXT,
    стоимость REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS договоры (
    айди UUID PRIMARY KEY NOT NULL,
    клиент_айди UUID NOT NULL,
    айди_страховки INTEGER NOT NULL,
    FOREIGN KEY (клиент_айди) REFERENCES клиенты (айди),
    FOREIGN KEY (айди_страховки) REFERENCES виды_страховок (айди) 
);
''')

for i in range(50):
    db.execute(f'INSERT INTO клиенты (айди, имя, фамилия) VALUES ("{uuid4()}", "{gen_str(6)}", "{gen_str(6)}")')
    db.execute(f'INSERT INTO виды_страховок (наименование, стоимость) VALUES ("{gen_str(6)}", "{gen_str(6)}")')
    db.execute(f'INSERT INTO договоры (айди, клиент_айди, айди_страховки) VALUES ("{uuid4()}", '
               f'"{all_uuid[randint(0, i)]}", {randint(0, i)})')
