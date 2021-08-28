import logging
import sqlite3
import enum
import os

_log = logging.getLogger()


class DBConnection:
    class States(enum.Enum):
        """Data base connection status"""
        INIT = 'init'
        CONNECTED = 'connected'
        RUNNING = 'running'
        CLOSED = 'closed'
        ERROR = 'error'

    def __init__(self, db_name='activities.db', db_path=''):
        """
        Provide helpers for sqlite db connection

        Parameters
        ----------
        db_name:
            str database name
        db_path:
            str absolute  db path where db will be stored
        """
        self.name = db_name
        self.db_path = db_path if db_path else os.getcwd()
        self.state = self.States.INIT
        self._connection = None
        self._cursor = None

    def __del__(self):
        """Close all connections"""
        if self.state != self.States.CLOSED:
            self._connection.close()

    def connect(self):
        """Try to connect or create a new database"""
        try:
            if not os.path.exists(self.db_path):
                os.makedirs(self.db_path)
            self._connection = sqlite3.connect(os.path.join(self.db_path, self.name))
            self._cursor = self._connection.cursor()
            self.state = self.States.CONNECTED
            _log.info("Connected to {}".format(os.path.join(self.db_path, self.name)))
        except Exception as e:
            _log.error('Could not connect to database: {}'.format(e))

    def close(self):
        """Close connection to the database"""
        self._connection.close()
        self._cursor = None
        self.state = self.States.CLOSED

    def create_table(self, table_name, table_columns):
        """
        Create table into the database. If table already exists, pass

        Parameters
        ----------
        table_name:
            Table name to create
        table_columns:
            str Columns names and types inside new table.
            example :'start_time text, end_time text'

        Returns
        -------
        None
        """
        try:
            self._cursor.execute("""CREATE TABLE {} ({})""".format(table_name, table_columns))
            self._connection.commit()
        except Exception as e:
            _log.error("Could not create table {} : {}".format(table_name, e))

    @property
    def connection(self):
        return self._connection

    def insert_entry_to_table(self, table, entry, values):
        """
        Insert new entry to table

        Parameters
        ----------
        table:
            table name
        entry:
            dict containing value names as  keys and values values as values (lol)
                example: dict(start_time='0.5', end_time='0.6', days=0)
        values:
            str values in the table
                example: ':start_time, :end_time, :days'

        Returns
        -------
        None
        """
        if self.state == self.States.CONNECTED:
            try:
                self._cursor.execute(f"INSERT INTO {table} VALUES ({values})".format(table=table, values=values),
                                     entry)
                self._connection.commit()
                _log.info('Entry added to table {}: {}'.format(table, entry))
            except Exception as e:
                _log.error('Failed to insert data into table {}: {}'.format(table, e))
        else:
            _log.error('Cannot insert entry into to a clossed connection')


