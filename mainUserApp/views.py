from sqlite3 import DatabaseError

from django.shortcuts import render
import pyodbc
import platform
import socket
import os
import psutil
import getpass
import mysql.connector

def get_Data_from_db():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=TDMS01;DATABASE=TDMS_TATBEL;UID=sa;PWD=sa')
        cursor = conn.cursor()
        query = """
            SELECT F_MAIL
            FROM TUser
            """
        cursor.execute(query)
        rows = cursor.fetchall()
    except DatabaseError as e:
        print(f'Ошибка при запросе к внешней базе данных: {e}')
        rows = []
    return rows


def get_computer_info():
    info = {
        'MachineName': platform.node(),
        'OSVersion': platform.platform(),
        'IP_Address': socket.gethostbyname(socket.gethostname()),
        'Domain': socket.getfqdn().split('.', 1)[-1],
    }
    return info

def get_user_info():
    user_info = {
        'UserName': os.getlogin(),
        'UserDomain': os.getenv('USERDOMAIN'),
        'Hostname': socket.gethostname(),
        'FullUsername': f"{os.getenv('USERDOMAIN')}\\{os.getlogin()}",
        'LoggedInUser': getpass.getuser()
    }
    return user_info

def seacrh_user_data(FullUsername):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=TDMS01;DATABASE=TDMS_TATBEL;UID=sa;PWD=sa')
    cursor = conn.cursor()

    load_user = f"""
             SELECT F_DESCR, F_MAIL
             FROM TUser
             WHERE F_LOGIN = '{FullUsername}'
             """
    cursor.execute(load_user)
    user = cursor.fetchone()
    return user[0]


def search_timeID_user(user):
    config = {
        'user': 'root',
        'password': '',
        'port':'3305',
        'host': '10.100.7.12',
        'database': 'tc-db-main',
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query_user_id = f"""
    SELECT ID 
    FROM personal
    WHERE NAME = '{user}'
    """
    cursor.execute(query_user_id)
    user_info = cursor.fetchone()
    print(f"Вы подключены к базе данных: {user_info}")

    cursor.close()
    cnx.close()
    return user_info[0]


def view_data_from_db(request):
    user_info = get_user_info()
    userName = seacrh_user_data(user_info['FullUsername'])
    data = search_timeID_user(userName)
    context = {
        'data': data,
        'userName': userName
    }
    return render(request, 'mainUserApp/home.html', context)
