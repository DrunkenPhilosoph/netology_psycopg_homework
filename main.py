import psycopg2

def create_table(conn):
    create_db = '''
    CREATE TABLE client (id SERIAL PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), email VARCHAR(255));
    CREATE TABLE client_phone (phone VARCHAR(20), client_id INT REFERENCES client (id))
    '''
    conn.cursor().execute(create_db)
    conn.commit()
    return f'''Созданы таблицы: 1. Название client столбцы: id, name, surname, email
                                2. Название client_phone столбцы: phone, client_id'''

def add_client(conn, client_name, client_surname, client_email, phone=None):
    cursor = conn.cursor()
    add_client = f'''
    INSERT INTO public.client (name, surname, email) VALUES ('{client_name}', '{client_surname}', '{client_email}') RETURNING id;
    '''
    cursor.execute(add_client)
    client_id = cursor.fetchone()
    if phone != None:
        add_client_phone = f'''
            INSERT INTO public.client_phone (phone, client_id) VALUES ('{phone}', '{client_id[0]}')
        '''
        cursor.execute(add_client_phone)
    else:
        phone = 'Без номера'

    conn.commit()
    return f'Успешно добавлена запись: {client_id[0]}, {client_name}, {client_surname}, {client_email}, {phone}'

def add_client_phone(conn, phone, client_id):
    cursor = conn.cursor()
    search_client = f'''
    SELECT id, name 
    FROM public.client
    WHERE id = {client_id}
    '''
    cursor.execute(search_client)
    search_result = cursor.fetchone()
    if search_result != None:
        if client_id == search_result[0]:
            add_client_phone = f'''
                        INSERT INTO public.client_phone (phone, client_id) VALUES ('{phone}', '{client_id}')
                    '''
            cursor.execute(add_client_phone)
            conn.commit()
            return f'Номер {phone} к клинту с id: {client_id} успешно добавлен'
    else:
        return f'Клиента с идентификатором: {client_id} не существует!'

def change_client_info(conn, client_id, client_name=None, client_surname=None, client_email=None, phone=None):
    cursor = conn.cursor()
    search_client = f'''
    SELECT id, name, surname, email, phone
    FROM public.client c
    left join public.client_phone cp on cp.client_id = c.id
    WHERE id = {client_id}
    '''
    cursor.execute(search_client)
    search_result = cursor.fetchall()
    l = []
    if search_result != l:
        if phone != None:
            phones_list = []
            for i, iter_phone in enumerate(search_result):
                phones_list.append([i, iter_phone])
            for select in phones_list:
                print(f'№:{select[0]}.', select[1][4])
            select_phone = int(input(
                f'У клиента c id {len(search_result)} номеров телефонов. Выберите номер который нужно заменить у клиента c id {client_id}:'))
            if select_phone <= len(phones_list) - 1:
                change_phone = f'''
                UPDATE public.client_phone
                SET phone = '{phone}'
                WHERE client_id = '{client_id}' and phone = '{phones_list[select_phone][1][-1]}';
                '''
                res = cursor.execute(change_phone)
            else:
                return f'Выбран неправильный № попробуйте снова'
        if client_email != None:
            change_email = f'''
            UPDATE public.client
            SET email = '{client_email}'
            WHERE id = '{client_id}';
            '''
            res = cursor.execute(change_email)
        if client_surname != None:
            change_email = f'''
            UPDATE public.client
            SET surname = '{client_surname}'
            WHERE id = '{client_id}';
            '''
            res = cursor.execute(change_email)
        if client_name != None:
            change_email = f'''
            UPDATE public.client
            SET name = '{client_name}'
            WHERE id = '{client_id}';
            '''
            cursor.execute(change_email)
        conn.commit()
        return f'Данные клиента успешно изменены'
    else:
        return f'Клиента с id {client_id} не существует'

def delete_phone(conn, client_id):
    cursor = conn.cursor()
    search_client = f'''
    SELECT client_id, phone
    FROM public.client_phone 
    WHERE client_id = {client_id}
    '''
    cursor.execute(search_client)
    search_result = cursor.fetchall()
    phones_list = []
    l = []
    if search_result != l:
        for i, iter_phone in enumerate(search_result):
            i += 1
            print(i -1, 'Телефон:', iter_phone[1])
            phones_list.append([f'№:{iter_phone[0]}.', iter_phone[1][4]])
        select_phone = int(input(
            f'У клиента {len(search_result)} номеров телефонов. Выберите номер который нужно удалить у клиента c id {client_id}:'))
        if select_phone <= len(phones_list) - 1:
            delete_phone = f'''
            DELETE FROM public.client_phone
            WHERE client_id = '{client_id}' and phone = '{phones_list[select_phone][1][-1]}';
            '''
            cursor.execute(delete_phone)
            conn.commit()
        else:
            return 'Выбран неправильный № попробуйте снова'
        return f'Телефон клиента c id {client_id} успешно удален'
    else:
        return f'Клиента с id {client_id} не существует'

def delete_client(conn, client_id):
    cursor = conn.cursor()
    search_client = f'''
    SELECT id, name, surname, email, phone
    FROM public.client c
    left join public.client_phone cp on cp.client_id = c.id
    WHERE id = {client_id}
    '''
    cursor.execute(search_client)
    search_result = cursor.fetchall()
    l = []
    if search_result != l:
        delete_all_client = f'''
                DELETE FROM public.client_phone
                WHERE client_id = '{client_id}';
                DELETE FROM public.client WHERE id = {client_id};
                '''
        cursor.execute(delete_all_client)
        conn.commit()
        return f'Клиент с id {client_id} успешно удален'
    else:
        return f'Клиента с id {client_id} не существует'

def find_client(conn, client_name=None, client_surname=None, client_email=None, phone=None):
    cursor = conn.cursor()
    search_client = f'''
    SELECT id, name, surname, email, phone
    FROM public.client c
    left join public.client_phone cp on cp.client_id = c.id
    WHERE name = '{client_name}' or phone = '{phone}' or surname = '{client_surname}' or email = '{client_email}';
    '''
    cursor.execute(search_client)
    search_result = cursor.fetchall()
    l = []
    if search_result != l:
        result = ''
        for i in search_result:
            result += f'ID Клиента: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Адрес электронной почты: {i[3]}, Номер телефона: {i[4]}\n'
        return result
    else:
        return f'Клиент не найден'










with psycopg2.connect(database='postgres', user='postgres', password='1234', host='localhost', port=5433) as conn:
    create_table(conn)
    print(add_client(conn, 'Василиса', 'Прекрасная', 'test@yandex.ru', '965 (354) 803-34-64'))
    print(add_client(conn, 'Валерия', 'Воронова', 'test@test.ru', '211 (722) 791-70-54'))
    print(add_client(conn, 'Матвей', 'Кузнецов', 'mk@google.com', '595 (116) 473-52-24'))
    print(add_client(conn, 'Варвара', 'Лебедева', 'varavaraleb@yandex.ru', '79995554321'))
    print(add_client(conn, 'Илья', 'Золотарев', 'ilyazol@rambler.ru', '253 (183) 226-73-56'))
    print(add_client(conn, 'Софья', 'Короткова', 'sk@mail.ru', '591 (153) 594-55-14'))
    print(add_client_phone(conn, '212 (553) 788-94-67', 6))
    print(add_client_phone(conn, '386 (426) 198-13-15', 3))
    print(add_client_phone(conn, '79171234567', 2))
    print(change_client_info(conn, client_id=2, client_email='pepiko@yandex.ru', client_name='Валерия',
                             client_surname='Кудрявцева', phone='591 (153) 594-55-21'))
    print(delete_phone(conn, client_id=6))
    print(delete_client(conn, client_id=3))
    print(find_client(conn, client_surname='Короткова'))
    print(find_client(conn, phone='965 (354) 803-34-64'))
conn.close()