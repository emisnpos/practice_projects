import bcrypt
import connection

def hash_password(naked_password):
    hashed_bytes = bcrypt.hashpw(naked_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(naked_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(naked_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def insert_username_userpassword(cursor, username, password):
    hashed_password = hash_password(password)
    query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s);
            """
    cursor.execute(query, (username, hashed_password))

    # ez is egy jó megoldás
    # cursor.execute("""
    #       INSERT INTO users(username, password)
    #       VALUES (%(username)s, %(password)s)
    #   """, {'username': username, 'password': hashed_password})

@connection.connection_handler
def valid_password(cursor, username):
    cursor.execute("""
        SELECT password
        FROM users
        WHERE username = %(username)s
        """, {'username': username})
    return cursor.fetchone()
