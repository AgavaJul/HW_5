import psycopg2

con = psycopg2.connect(
  database="agava", 
  user="postgres",
  password = "15PfVtxfybt")

with con.cursor() as cur:
        # cur.execute("""drop table phone;""")
        # con.commit()
        # cur.execute("""drop table client;""")
        # con.commit()

    def create_db(con):
        create_client = """CREATE TABLE client (id SERIAL PRIMARY KEY, first_name CHAR(100) NOT NULL, last_name CHAR(100) NOT NULL, email char(100) UNIQUE NOT NULL);"""
        cur.execute(create_client)
        con.commit()
        
        create_phone = """CREATE TABLE phone (id_client INT NOT NULL REFERENCES client (id), phone CHAR(12) UNIQUE NOT NULL CHECK (length(phone) = 12), PRIMARY KEY (id_client, phone));"""
        cur.execute(create_phone)
        con.commit()
        print('База данных успешно создана')
      
    def add_client(con, first_name, last_name, email): #добавление нового клиента
        cur.execute("""INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;""", (first_name, last_name, email))
        print('id клиента', cur.fetchone()[0])
        con.commit()
    # print("Данные о клиенте успешно сохранены")

    def add_phone(con, id_client, phone): #добавление телефона/телефонов
        cur.execute("""INSERT INTO phone (id_client, phone) VALUES (%s, %s);""", (id_client, phone))
        con.commit()
        print ('Номер телефона успешно добавлен')

    def change_client(con, id_client, first_name, last_name, email): #Функция, позволяющая изменить данные о клиенте
        cur.execute("""UPDATE client SET first_name = %s, last_name = %s, email = %s WHERE id = %s;""", (first_name, last_name, email, id_client))
        con.commit()
        print('Данные успешно изменены')

    def delete_phone(con, id_client, phone): #Функция, позволяющая удалить телефон для существующего клиента
        cur.execute("""DELETE FROM phone WHERE id_client = %s and phone = %s;""", (id_client, phone))
        con.commit()
        print('Номер телефона успешно удален')

    def delete_client(con, id):
        cur.execute("""DELETE FROM phone WHERE id_client = %s;""", (id))
        con.commit()
        cur.execute("""DELETE FROM client WHERE id = %s;""", (id))
        con.commit()
        print('Данные успешно удалены')

    def find_client(con, first_name=None, last_name=None, email=None, phone=None):
        cur.execute("""SELECT c.*, p.phone FROM client c FULL JOIN phone p ON c.id = p.id_client WHERE first_name = %s OR last_name = %s OR email = %s OR phone = %s;""", (first_name, last_name, email, phone))  
        
        rows = cur.fetchall()  
        for row in rows:  
            print("id =", row[0])
            print("first_name =", row[1])
            print("last_name =", row[2])
            print("email =", row[3])
            print("phone =", row[4], "\n")
    
    
    # create = create_db(con) #вызов функции на создание БД
   
    # add_client = add_client(con, 'Мария', 'Сатонкина', 'yahanya@mail.ru') # вызов функции на добавление нового клиента
    
    # add_phone = add_phone(con, 1, '+79131211777') #вызов функции для добавления номера телефона
    
    # CC = change_client(con, first_name = "Василий", last_name = "Пупкин", email = "pupok@py.ru", id_client = 1) # вызов функции для изменения данных о клиенте

    # DP = delete_phone(con, 10, '+79131211777') # вызов функции для удаления номера телефона

    # DC = delete_client(con, (1,)) # вызов функции для удаления данных о клиенте

    # fc = find_client(con, email = 'yahanya@mail.ru') # вызов функции для поиска 

con.close()