import pymysql

def setupDB():
    db = pymysql.connect(host="localhost", user="flask_user", password="password")
    cursor = db.cursor()

    try:
        with open("db_init", "r") as f:
            sql_commands = f.read()
            for command in sql_commands.split(";"):
                if command.strip():
                    cursor.execute(command)

        db.commit()
        print("Database and table setup complete!")
    except Exception as e:
        print(f"Error setting up database: {e}")
    finally:
        cursor.close()
        db.close()
        print("Database and table setup complete!")