import psycopg2

from dbtcontractgen.connection.base import DatabaseConnection


class PostgreSQLConnection(DatabaseConnection):
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        self.cursor = self.conn.cursor()

    def run_query(self, query: str):
        with self.cursor as cursor:
            cursor.execute(query)
            return cursor.fetchall()
