import sqlite3

def db_connection(func):
    def warp(*args):
        global conn
        conn = sqlite3.connect('line.db')
        output = func(*args)
        if conn is not None:
            conn.close()

        return output
    return warp

@db_connection
def read_user_action(line_user_id):
    sql = f"SELECT `line_user_id`, `previous_action` from `users` WHERE `line_user_id`='{line_user_id}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    return data[1] if data else None

@db_connection
def read_user_data(line_user_id, line_user_name):
    sql = f"SELECT `line_user_id`, `line_user_name`, `weight`, `height`, `age` from `users` WHERE `line_user_id`='{line_user_id}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    if not data:
        sql = f"INSERT INTO `users` (`line_user_id`, `line_user_name`) VALUES ('{line_user_id}', '{line_user_name}')"
        cursor.execute(sql)
        conn.commit()
        sql = f"SELECT `line_user_id`, `line_user_name`, `weight`, `height`, `age` from `users` WHERE `line_user_id`='{line_user_id}'"
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
    return data

@db_connection
def update_user_action(line_user_id, action):
    sql = f"UPDATE `users` set `previous_action`='{action}' WHERE `line_user_id`='{line_user_id}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

@db_connection
def update_user_weight(line_user_id, weight):
    sql = f"UPDATE `users` set `weight`='{weight}' WHERE `line_user_id`='{line_user_id}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

@db_connection
def update_user_height(line_user_id, height):
    sql = f"UPDATE `users` set `height`='{height}' WHERE `line_user_id`='{line_user_id}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

@db_connection
def update_user_age(line_user_id, age):
    sql = f"UPDATE `users` set `age`='{age}' WHERE `line_user_id`='{line_user_id}'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()