import pymysql
import config

category = ['生育及育兒','學生','國民年金及勞工','中低收入','身心障礙','長者','房屋','親屬身故給付',"其他"]
location_dict = {
    "北部": ["臺北","新北","基隆","新竹","桃園","宜蘭"],
    "中部": ["苗栗","臺中","彰化","南投","雲林"],
    "南部": ["高雄","臺南","嘉義","屏東"],  
    "東部": ["花蓮","臺東"],
    "外島":["金門","馬祖","澎湖"]
}

category_dict = {
    "生育及育兒":"birth",
    "學生":"students",
    "國民年金及勞工":"labor",
    "中低收入":"lowincome",
    "身心障礙":"disabled",
    "長者":"elder",
    "房屋":"house",
    "親屬身故給付":"passaway",
    "其他":"other"
}

db_settings = {
    "host": config.DB_HOST,
    "port": int(config.DB_PORT),
    "user": config.DB_USER,
    "password": config.DB_PASSWORD,
    "db": config.DB_SCHEMA,
    "charset": "utf8"
}

def searchByCode(code):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
             command = "SELECT * FROM "+config.DB_SCHEMA+"."+config.DB_TABLE+" WHERE serial_no = %s"
             cursor.execute(command, (code,))
             result = cursor.fetchone()
             return result
    except Exception as ex:
        print(ex)
        return 'Error'

def searchByCategoryAndLocation(category,location):
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
             
             command = "SELECT * FROM "+config.DB_SCHEMA+"."+config.DB_TABLE+" WHERE category LIKE %s AND (organization_name LIKE %s OR organization_name = '中央政府')"
             cursor.execute(command, ('%' + category + '%','%' + location + '%'))
             result = cursor.fetchall()
             return result
        
    except Exception as e:
        print("=========================")
        print("Exception: ",e)
        print("=========================")
        return 'Error'