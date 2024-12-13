import sqlite3
DATABASE = 'Todo App using Flask with SQLite 3/todo.db'

def get_connection():
    connection = sqlite3.connect(DATABASE)
    return connection

def run_query(connection, query, operation):
    data = None
    operation_success = False

    cursor = connection.cursor()
    try:
        cursor.execute(query)

        if operation == "select":
            data = cursor.fetchall()

        elif operation in ["insert", "delete", "update"]:
            connection.commit()
            if cursor.rowcount > 0:
                operation_success = True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()

    return data, operation_success

def execute_query(connection, query, operation):
    try:
        data, operation_success = run_query(connection, query, operation)

    except sqlite3.Error:
        connection = get_connection()
        data, operation_success = run_query(connection, query, operation)

    return data, operation_success

def initialize_db():
    connection = get_connection()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tasks (
        task_id TEXT PRIMARY KEY NOT NULL,
        task TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_updated_at TEXT,
        status TEXT NOT NULL
    )
    """
    run_query(connection, create_table_query, "create")
    connection.close()

initialize_db()