import luigi
from sqlalchemy import engine

class SQLiteTableTarget(luigi.Target):
    '''Target to verify if a SQLite table exists, independant of last update'''

    def __init__(self, table: str, eng: engine.Engine):
        super().__init__()
        self._table = table
        self._eng = eng


    # The exists method will be checked by luigi to ensure the Tasks that
    # output this target has been completed correctly
    def exists(self):
        query = '''SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}' '''
        query_set = self._eng.execute(query.format(table_name=self._table))
        return query_set.fetchone() is not None