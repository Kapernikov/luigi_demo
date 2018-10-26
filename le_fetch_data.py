import requests
import csv
import pandas as pd
import json
import luigi
from luigi.contrib import sqla
import datetime
from le_utils import *
import sqlalchemy
from le_targets import *
from le_create_db import CreateDB

class GetEQData(luigi.Task):
    '''Task to get the earthquakes data from USGS website and send them to
    the specified database'''

    # Defaulting to the eq engine, linked to the eq_db sqlite database
    engine_name = luigi.Parameter(default='eq')

    def requires(self):
        return CreateDB(db_file_name=MAIN_DB_PATH)

    def output(self):
        return SQLiteTableTarget(table='earthquakes', eng=DB_ENGINES[self.engine_name])

    def run(self):
        data = pd.read_csv(os.path.join('data', 'eq_data.csv'))
        # Because dates are parsed as text by pandas
        data.time = pd.to_datetime(data.time, format='%Y-%m-%dT%H:%M:%S.%f')
        # The engine_name is mapped to an actual engine object via dict lookup
        data.to_sql('earthquakes', con=DB_ENGINES[self.engine_name], if_exists='replace', index=False)



