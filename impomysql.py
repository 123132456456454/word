import pymysql

try:
    conn = pymysql.connect(
        host="192.168.57.149",
        user="app_user",
        password="strong_password",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 返回字典格式数据
    )
    with conn.cursor() as cursor:
        cursor.execute("SHOW databases")
        tables = cursor.fetchall()
        print(f"✅ 连接成功！数据库表列表: {[tables]}")
except pymysql.Error as e:
    print(f"❌ 连接失败: {e}")
finally:
    if conn:
        conn.close()