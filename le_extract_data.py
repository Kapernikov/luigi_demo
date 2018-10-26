import pandas as pd
import json
import luigi
from luigi.contrib import sqla
import datetime
from le_utils import *
import sqlalchemy
from le_targets import *
from le_fetch_data import *
import os

class ExportAllQueries(luigi.WrapperTask):
    def requires(self):
        folders = [folder for folder in os.listdir(os.path.join(QUERIES_FOLDER))
                   if folder in DB_ENGINES]
        return [ExportQueriesInFolder(folder_name=folder) for folder in folders]


class ExportQueriesInFolder(luigi.WrapperTask):
    folder_name = luigi.Parameter(default='eq')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def requires(self):
        if self.folder_name in DB_ENGINES:
            files = os.listdir(os.path.join(QUERIES_FOLDER, self.folder_name))
            sql_files = [file for file in files if os.path.splitext(file)[1] == '.sql']

            return [
                ExportDataBasedOnQueryFile(query_file_name=sql_file,
                                           engine_name=self.folder_name)
                for sql_file in sql_files
            ]


class ExportDataBasedOnQueryFile(luigi.Task):
    query_file_name = luigi.Parameter()
    engine_name = luigi.Parameter(default='eq')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query_path = os.path.join(QUERIES_FOLDER, self.engine_name, self.query_file_name)

        #Get name of the file with extension
        _, self.input_query_file = os.path.split(self.query_path)

        #Get name of the file, without extension
        self.output_filename, _ = os.path.splitext(self.input_query_file)

        self.complete_filename = '{db_source}_{output_name}.xlsx'.format(db_source=self.engine_name,
                                                                         output_name=self.output_filename)

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_FOLDER,
                                              self.complete_filename))

    def requires(self):
        return GetEQData()

    def run(self):
        if not os.path.isdir(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)

        with open(self.query_path, 'r') as query_file_handle:
            query = query_file_handle.read()

        extracted_data=pd.read_sql(query,
                                   con=DB_ENGINES[self.engine_name])

        extracted_data.to_excel(os.path.join(OUTPUT_FOLDER, self.complete_filename), index=False)


