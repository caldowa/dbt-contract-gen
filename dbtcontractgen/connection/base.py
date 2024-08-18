import logging
from abc import ABC, abstractmethod


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
    def run_query(self, query: str) -> tuple:
        """Run a query on the database and return the results."""
        pass

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is not None:
                logging.error(f"An error occurred: {exc_value}, {traceback}")
                if self.conn:
                    self.conn.rollback()
            else:
                if self.conn:
                    self.conn.commit()
        finally:
            self.close()
