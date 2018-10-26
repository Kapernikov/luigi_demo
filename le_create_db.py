import sqlite3
import luigi

class CreateDB(luigi.Task):
    db_file_name=luigi.Parameter()

    def requires(self):
        pass

    def output(self):
        return luigi.LocalTarget(self.db_file_name)

    def run(self):
        with sqlite3.connect(self.db_file_name) as c:
            pass

