import pymysql
import config

category = ['生育及育兒','學生','國民年金及勞工','中低收入','身心障礙','長者','房屋','親屬身故給付']

db_settings = {
    "host": config.DB_HOST,
    "port": int(config.DB_PORT),
    "user": config.DB_USER,
    "password": config.DB_PASSWORD,
    "db": config.DB_SCHEMA,
    "charset": "utf8"
}

def searchByName(name):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
             command = "SELECT * FROM "+config.DB_SCHEMA+"."+config.DB_TABLE+" WHERE name = %s"
             cursor.execute(command, (name,))
             result = cursor.fetchone()
             return result
    except Exception as ex:
        print(ex)
        return 'Error'

def searchByCategory(category):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
             command = "SELECT * FROM "+config.DB_SCHEMA+"."+config.DB_TABLE+" WHERE category = %s"
             cursor.execute(command, (category,))
             result = cursor.fetchall()
             return result
    except Exception as ex:
        print(ex)
        return 'Error'