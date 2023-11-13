#pylint: disable=import-error, redefined-outer-name
import json
import os

import psycopg2

class PostgresInteraction():
    def __init__(self, host: str, dbname: str, user: str, password: str, table: str=os.getenv("POSTGRES_TABLE")):
        """Class for handling connections to a PostgreSQL database."""
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.table = table
        self.conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(self.host, self.user, self.dbname, self.password, "require")
        self.conn: psycopg2.extensions.connection=None,
        self.cursor: psycopg2.extensions.cursor=None

    def open_cursor_and_conn(self):
        """Get cursor to postgres database."""
        self.conn = psycopg2.connect(self.conn_string)
        print("Connection established")
        self.cursor = self.conn.cursor()

    def close_cursor_and_conn(self):
        """Close cursor to postgres database."""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print("Connection closed")

    def _get_all_entries(self):
        """Get all entries from postgres database."""
        self.open_cursor_and_conn()
        # Create a table
        self.cursor.execute("SELECT * FROM rezepte")
        rows = self.cursor.fetchall()

        self.close_cursor_and_conn()
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

        self.open_cursor_and_conn()

        # Create a table (if not exists)
        field_types = (
            "name VARCHAR(50), "
            "course VARCHAR(30), "
            "description VARCHAR(1000), "
            "source VARCHAR(100), "
            "season VARCHAR(30), "
            "style VARCHAR(30)"
        )
        create_query = f"CREATE TABLE IF NOT EXISTS rezepte (id serial PRIMARY KEY, {field_types});"
        self.cursor.execute(create_query)
        print("Finished creating table")

        # Insert data into the table
        field_names = "name, course, description, source, season, style"
        field_values = (name, course, description, source, season, style)
        insert_query = f"INSERT INTO rezepte ({field_names}) VALUES {field_values};"
        self.cursor.execute(insert_query)
        print("Inserted 1 rows of data")

        # Remove duplicates
        print("Removing duplicates")
        delete_query = """
            DELETE FROM rezepte a USING rezepte b
            WHERE a.ctid < b.ctid
            AND a.name = b.name
            AND a.course = b.course
            AND a.description = b.description
            AND a.source = b.source
            AND a.season = b.season
            AND a.style = b.style;
        """
        self.cursor.execute(delete_query)
        self.close_cursor_and_conn()

    def extract_data_from_postgres(self):
        """Extract data from postgres database for app."""
        rows = self._get_all_entries()
        fields = ['id', 'name', 'course', 'description', 'source', 'season', 'style']
        return [dict(zip(fields, row)) for row in rows]

    def delete_database(self):
        """Delete database."""
        self.open_cursor_and_conn()
        # Create a table
        self.cursor.execute("DROP TABLE IF EXISTS rezepte")
        print("Finished dropping table")
        self.close_cursor_and_conn()

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
