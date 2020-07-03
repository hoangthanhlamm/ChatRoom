import pyodbc
import logging


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(funcName)s '
                           ': line %(lineno)d :: %(message)s', level=logging.DEBUG)
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-02EF015\SQLEXPRESS;'
                      'Database=CompanyManager;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


class InitDB():
    async def create_db(self):
        query = 'if not exists (select * from sysobjects where name=\'Account\' and xtype=\'U\')' \
                'create table Account (' \
                'username varchar(30) primary key,' \
                'hash_password varchar(120) not null,' \
                'email varchar(50) not null)'
        cursor.execute(query)

        query = 'if not exists ( select * from sysobjects where name=\'Message\' and xtype=\'U\')' \
                'create table Message (' \
                'id int identity primary key,' \
                'sender varchar(30) not null,' \
                'time datetime not null,' \
                'msg varchar(200),' \
                'constraint FK_sender foreign key (sender) references Account(username))'
        cursor.execute(query)
        conn.commit()


class Account():
    async def get_user(self, username):
        query = 'Select * from Account where username = ?'
        query_args = [username, ]
        cursor.execute(query, query_args)
        if cursor.rowcount == 0:
            return None

        for row in cursor:
            user = {
                "username": row[0],
                "hash_password": row[1],
                "email": row[2]
            }
            return user
        return None

    async def create_user(self, username, hash_password, email):
        query = 'Insert into Account values (?, ?, ?)'
        query_args = [username, hash_password, email]
        result = "Success"
        try:
            cursor.execute(query, query_args)
            conn.commit()
        except Exception as err:
            result = "Fail"
            logging.error(err)
        return result


class Message():
    async def save_msg(self, sender, time, msg):
        query = 'Insert into Message (sender, time, msg) values (?, ?, ?)'
        query_args = [sender, time, msg]
        result = "Success"
        try:
            cursor.execute(query, query_args)
            conn.commit()
        except Exception as err:
            result = "Fail"
            logging.error(err)
        return result

    async def load_msg(self, max_message):
        query = 'Select Account.username, Message.time, Message.msg ' \
                'from Account, Message ' \
                'where Account.username = Message.sender ' \
                'order by Message.time ' \
                'offset (Select count(*) from Message) - {} row ' \
                'fetch first {} row only'.format(max_message, max_message)
        list_msg = []
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                msg = {
                    "sender": row[0],
                    "time": row[1],
                    "msg": row[2]
                }
                list_msg.append(msg)
        except Exception as err:
            list_msg = None
            logging.error(err)
        return list_msg

