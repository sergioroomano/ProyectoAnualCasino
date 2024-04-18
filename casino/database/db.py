import pymysql

def get_db_connection():
    connection = pymysql.connect(host='mascaro101.mysql.pythonanywhere-services.com',
                                 user='mascaro101',
                                 password='laquegana123',
                                 db='mascaro101$CasinoDB',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_users_table():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
            )
        ''')
        cursor.execute(sql)
    connection.commit()
    connection.close()