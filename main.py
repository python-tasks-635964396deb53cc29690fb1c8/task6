import sys
from base64 import b64encode
from random import randbytes, randint
from sqlite3 import connect
from uuid import uuid4

all_uuid = []


def gen_client_uuid() -> str:
    u = uuid4()
    all_uuid.append(u)
    return str(u)


def gen_str(_len: int) -> str:
    c_uuid = b64encode(randbytes(_len)).decode()
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


def insert_random_20():
    for i in range(20):
        db.execute(f'INSERT INTO клиенты (айди, имя, фамилия) VALUES ("{gen_client_uuid()}", "{gen_str(6)}", "{gen_str(6)}")')
        db.execute(f'INSERT INTO виды_страховок (наименование, стоимость) VALUES ("{gen_str(6)}", "{gen_str(6)}")')
        db.execute(f'INSERT INTO договоры (айди, клиент_айди, айди_страховки) VALUES ("{uuid4()}", '
                    f'"{all_uuid[randint(0, i)]}", {randint(1, i+1)})')
        db.commit()


def select_table(tb_name: str) -> list[tuple]:
    values = []
    for row in db.execute(f'SELECT * FROM {tb_name}'):
        values.append(row)
    return values


def _ins_str(s: str | int = "", sep: bool = False) -> str:
    return f'"{s}"{"," if sep else ""}'


def insert_table(tb_name: str, tb_values: str, v1: str, v2: str, _id: bool = True):
    print(f'INSERT INTO {tb_name} ({tb_values}) VALUES ({_ins_str(str(uuid4()), sep=True) if _id else ""}"{v1}", {v2 if v2.isdigit() else _ins_str(v2)})', file=sys.stderr)
    db.execute(
        f'INSERT INTO {tb_name} ({tb_values}) VALUES ({_ins_str(str(uuid4()), sep=True) if _id else ""}"{v1}", {v2 if v2.isdigit() else _ins_str(v2)})')
    db.commit()
