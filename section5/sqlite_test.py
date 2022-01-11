import sqlite3


class _Queries:
    create_table = """
        CREATE TABLE users (
            id int, 
            username text, 
            password text
        );"""

    insert_user = """INSERT INTO users VALUES (?, ?, ?)"""
    

if __name__ == '__main__':

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(_Queries.create_table)

    user = (1, 'alex', 'asdf')
    cursor.execute(_Queries.insert_user, user)

    users = [
        (2, 'hannah', 'taytay'),
        (3, 'bob', 'srhg')
    ]
    cursor.executemany(_Queries.insert_user, users)

    connection.commit()
    connection.close()