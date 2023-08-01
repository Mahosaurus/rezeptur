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
    field_types = "name VARCHAR(15), course VARCHAR(10), description VARCHAR(1000), source VARCHAR(100), season VARCHAR(10), style VARCHAR(30)"
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
    if course not in ("starter", "main", "dessert"):
        raise ValueError("Course must be one of: starter, main, dessert")

def check_season(season: str):
    if season not in ("spring", "summer", "autumn", "winter", "all"):
        raise ValueError("Season must be one of: spring, summer, autumn, winter, all")

if __name__ == "__main__":
    host = ""
    dbname = ""
    user = ""
    password = ""
    sslmode = "require"
    delete_database(host, dbname, user, password, sslmode)
    data = {"name": "Gemüsecurry", "course": "main", "description": "Standard Gemüsecurry", "source": "Erfahrung", "season": "all", "style": "asiatisch"}
    send_data_to_postgres(host, dbname, user, password, data)
    # data2 = {"name": "test2", "course": "main", "description": "test2", "source": "test2", "season": "summer", "style": "test2"}
    # send_data_to_postgres(host, dbname, user, password, data2)
    # show_database(host, dbname, user, password)
    # print(extract_data_from_postgres(host, dbname, user, password))
