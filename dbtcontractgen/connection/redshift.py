import redshift_connector

from dbtcontractgen.connection.base import DatabaseConnection


class RedsiftConnection(DatabaseConnection):
    def connect(self):
        self.conn = redshift_connector.connect(
            host=self.host, database=self.database, user=self.user, password=self.password, port=self.port
        )
        self.cursor = self.conn.cursor()

    def run_query(self, query: str):
        with self.cursor as cursor:
            cursor.execute(query)
            return cursor.fetchall()
