import os

import psycopg2


def send_data_to_postgres(host: str, dbname: str, user: str, password: str, data: dict):
    """Send data to postgres database."""
    name        = data["name"]
    course      = data["course"]
    description = data["description"]
    source      = data["source"]
    season      = data["season"]
    style       = data["style"]

    # Data check:
    check_course(course)
    check_season(season)

    # Update connection string information
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()
    # Create a table
    field_types = "name VARCHAR(50), course VARCHAR(30), description VARCHAR(1000), source VARCHAR(100), season VARCHAR(30), style VARCHAR(30)"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS rezepte (id serial PRIMARY KEY, {field_types});")
    print("Finished creating table")

    # Insert data into the table
    field_names = "name, course, description, source, season, style"
    field_values = (name, course, description, source, season, style)
    cursor.execute(f"INSERT INTO rezepte ({field_names}) VALUES {field_values};")
    print("Inserted 1 rows of data")

    conn.commit()

    cursor.close()
    conn.close()

def extract_data_from_postgres(host: str, dbname: str, user: str, password: str):
    # Update connection string information
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()
    # Create a table
    cursor.execute("SELECT * FROM rezepte")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    fields = ['id', 'name', 'course', 'description', 'source', 'season', 'style']

    return [dict(zip(fields, row)) for row in rows if row[0] != 0]


def delete_database(host: str, dbname: str, user: str, password: str, data: str):
    # Update connection string information
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()
    # Create a table
    cursor.execute("DROP TABLE IF EXISTS rezepte")
    print("Finished killing table")

    conn.commit()

    cursor.close()
    conn.close()

def show_database(host: str, dbname: str, user: str, password: str):
    # Update connection string information
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

    conn = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = conn.cursor()
    # Create a table
    cursor.execute("SELECT * FROM rezepte")
    rows = cursor.fetchall()
    print(rows)

    cursor.close()
    conn.close()

def fix_entries():
    pass #TODO: implementation

def check_course(course: str):
    if course not in ("starter", "main", "dessert", "other"):
        raise ValueError("Course must be one of: starter, main, dessert, other")

def check_season(season: str):
    if season not in ("spring", "summer", "autumn", "winter", "other"):
        raise ValueError("Season must be one of: spring, summer, autumn, winter, other")

if __name__ == "__main__":

    host = os.environ["POSTGRES_HOST"]
    dbname = os.environ["POSTGRES_DBNAME"]
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    sslmode = "require"
    try:
        show_database(host, dbname, user, password)
    except:
        pass
    delete_database(host, dbname, user, password, sslmode)
    from food_data import data
    for entry in data:
        send_data_to_postgres(host, dbname, user, password, entry)
    show_database(host, dbname, user, password)
