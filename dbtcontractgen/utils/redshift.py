import redshift_connector


class RedshiftConnection:
    def __init__(self, host, database, user, password, port=5439):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    def __enter__(self):
        self.conn = redshift_connector.connect(
            host=self.host, database=self.database, user=self.user, password=self.password, port=self.port
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def run_query(self, query):
        with self.cursor as cursor:
            cursor.execute(query)
            return cursor.fetchall()
