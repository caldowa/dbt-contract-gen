from abc import ABC, abstractmethod

import psycopg2


class DatabaseConnection(ABC):
    def __init__(self, host: str, user: str, password: str, database: str, port: int):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None
        self.cursor = None

    @abstractmethod
    def connect(self):
        """Connect to the database."""
        pass

    @abstractmethod
    def run_query(self, query: str):
        """Run a query on the database and return the results."""
        pass

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type or exc_value or traceback:
            self.conn.rollback()
        else:
            self.conn.commit()
        if self.cursor:
            self.cursor.close()
        self.close()


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