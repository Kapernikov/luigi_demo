# This file will be imported from all the other files

# Basic imports
import sqlalchemy as sa
import os

# Main DB against which the queries will be run
MAIN_DB_PATH = 'eq_db.db'

# Mapping of string: sqlalchemy engines to manage connections to different
# databases via the use of luigi Parameters
DB_ENGINES = {
    'eq': sa.create_engine('sqlite:///{}'.format(MAIN_DB_PATH))
}

# Useful folder paths
OUTPUT_FOLDER = os.path.join('results')
QUERIES_FOLDER = os.path.join('queries')