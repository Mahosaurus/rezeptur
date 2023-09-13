#pylint: disable=import-error, redefined-outer-name
import json
import os

import psycopg2

class PostgresHandler:
    def __init__(self, host: str, dbname: str, user: str, password: str):
        self.conn = self._connect_to_postgres(host, dbname, user, password)

    def _connect_to_postgres(self, host: str, dbname: str, user: str, password: str) -> psycopg2.extensions.connection:
        """Connect to postgres database."""
        # Update connection string information
        sslmode = "require"
        # Construct connection string
        conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={sslmode}"

        conn = psycopg2.connect(conn_string)
        print("Connection established")
        return conn

    def _disconnect_from_postgres(self):
        """Disconnect from postgres database."""
        self.conn.close()

    def _get_all_entries(self):
        """Get all entries from postgres database."""
        cursor = self.conn.cursor()
        # Create a table
        cursor.execute("SELECT * FROM rezepte")
        rows = cursor.fetchall()

        cursor.close()
        return rows

    def send_data_to_postgres(self, data: dict):
        """Send data to postgres database."""
        name        = data["name"]
        course      = data["course"]
        description = data["description"]
        source      = data["source"]
        season      = data["season"]
        style       = data["style"]

        # Data check:
        self.check_course(course)
        self.check_season(season)

        cursor = self.conn.cursor()
        # Create a table (if not exists)
        field_types = "name VARCHAR(50), course VARCHAR(30), description VARCHAR(1000), source VARCHAR(100), season VARCHAR(30), style VARCHAR(30)"
        cursor.execute(f"CREATE TABLE IF NOT EXISTS rezepte (id serial PRIMARY KEY, {field_types});")
        print("Finished creating table")

        # Insert data into the table
        field_names = "name, course, description, source, season, style"
        field_values = (name, course, description, source, season, style)
        cursor.execute(f"INSERT INTO rezepte ({field_names}) VALUES {field_values};")
        print("Inserted 1 rows of data")

        self.conn.commit()

        # Remove duplicates
        print("Removing duplicates")
        cursor.execute("DELETE FROM rezepte a USING rezepte b WHERE a.ctid < b.ctid AND a.name = b.name AND a.course = b.course AND a.description = b.description AND a.source = b.source AND a.season = b.season AND a.style = b.style;")
        self.conn.commit()
        cursor.close()

    def extract_data_from_postgres(self):
        """Extract data from postgres database for app."""
        rows = self._get_all_entries()
        fields = ['id', 'name', 'course', 'description', 'source', 'season', 'style']
        return [dict(zip(fields, row)) for row in rows]

    def delete_database(self):
        """Delete database."""
        cursor = self.conn.cursor()
        # Create a table
        cursor.execute("DROP TABLE IF EXISTS rezepte")
        print("Finished dropping table")

        self.conn.commit()
        cursor.close()

    def export_database(self, export: bool=False) -> list:
        """Export database entries to json file."""
        rows = self._get_all_entries()

        fields = ['id', 'name', 'course', 'description', 'source', 'season', 'style']
        # Do not export "id"
        export_dict = [dict(zip(fields[1:], row[1:])) for row in rows]
        if export:
            with open("food_export.json", "w", encoding='utf-8') as filehandle:
                json.dump(export_dict, filehandle, ensure_ascii=False, indent=4)
        print("Finished exporting table")
        return export_dict

    def fix_entries(self):
        """Fix entries."""
        pass #TODO: implementation

    @staticmethod
    def check_course(course: str):
        """Check course, must be one of: starter, main, dessert, other."""
        if course not in ("starter", "main", "dessert", "other"):
            raise ValueError("Course must be one of: starter, main, dessert, other")

    @staticmethod
    def check_season(season: str):
        """Check season, must be one of: spring, summer, autumn, winter, other."""
        if season not in ("spring", "summer", "autumn", "winter", "other"):
            raise ValueError("Season must be one of: spring, summer, autumn, winter, other")

if __name__ == "__main__":
    # The flow
    host = os.environ["POSTGRES_HOST"]
    dbname = os.environ["POSTGRES_DBNAME"]
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    postgres_conn = PostgresHandler(host, dbname, user, password)

    # 1. Export and enter same data
    # try:
    #     postgres_conn.export_database(export=True)
    # except Exception as e:
    #     print(e)
    # with open("food_export.json", "r", encoding='utf-8') as filehandle:
    #     data = json.load(filehandle)
    # for entry in data:
    #     postgres_conn.send_data_to_postgres(entry)

    # Replace all entries in the database with the exported ones (manual fix)
    postgres_conn.delete_database()
    with open("food_export.json", "r", encoding='utf-8') as filehandle:
        data = json.load(filehandle)
    for entry in data:
        postgres_conn.send_data_to_postgres(entry)
