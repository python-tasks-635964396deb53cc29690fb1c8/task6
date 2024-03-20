#!/usr/bin/env python3
from main import select_table, insert_table, insert_random_20
from cgi import FieldStorage


form = FieldStorage()
tname = form.getvalue('tname', '')
v1 = form.getvalue('v1', '')
v2 = form.getvalue('v2', '')
rnd = form.getvalue('rnd', '')


if tname and v1 and v2:
    if tname == 'клиенты':
        insert_table(tname, 'айди, имя, фамилия', v1, v2)
    elif tname == 'договоры':
        insert_table(tname, 'айди, клиент_айди, айди_страховки', v1, v2)
    elif tname == 'виды_страховок':
        insert_table(tname, 'наименование, стоимость', v1, v2, False)
elif rnd:
    insert_random_20()


def get_html(tbname: str) -> str:
    html = ''
    values = select_table(tbname)
    for value in values:
        html += f'<tr>{"".join([f"<td>{td}</td>" for td in value])}</tr>'
    return html


print('Content-Type: text/html;charset=utf-8')
print()
print(f'''
<!DOCTYPE html>
<html>
<head>
    <title>OK</title>
    
    <style>
        main {{
            display: flex;
            flex-wrap: nowrap;
            justify-align: space-between;
        }}
        
        main table {{
            margin: 5px;
        }}
        
        header {{
            margin: 10px;
        }}
        
        form {{
            display: inline-block;
        }}
    </style>
</head>
<body>
    <header>
        <span>Добавить запись: </span>
        <form>
            <input placeholder="Название таблицы" name="tname">
            <input placeholder="Значение 1" name="v1">
            <input placeholder="Значение 2" name="v2">
            <input type="submit" value="Добавить">
        </form>
        <form>
            <input type="hidden" name="rnd" value="rnd">
            <input type="submit" value="Зарандомить">
        </form>
    </header>
    <main>
        <table border="1">
            <caption>Клиенты</caption>
            <tbody>
                <tr>
                    <th>Айди</th>
                    <th>Имя</th>
                    <th>Фамилия</th>
                </tr>
                {get_html('клиенты')}
            </tbody>
        </table>
        <table border="1">
            <caption>Виды страховок</caption>
            <tbody>
                <tr>
                    <th>Айди</th>
                    <th>Наименование</th>
                    <th>Стоимость</th>
                </tr>
                {get_html('виды_страховок')}
            </tbody>
        </table>
        <table border="1">
            <caption>Договоры</caption>
            <tbody>
                <tr>
                    <th>Айди</th>
                    <th>Айди клиента</th>
                    <th>Айди страховки</th>
                </tr>
                {get_html('договоры')}
            </tbody>
        </table>
    </main>
</body>
</html>
''')
