from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine

import pandas as pd 
import numpy as np 

import boto3
from argparse import ArgumentParser


DATA_DETAILS = {
    'event': {
        'filename': 'allevents_pipe.txt',
        'col_names': ['event_id', 'venue_id', 'cat_id',
                             'date_id', 'event_name', 'start_time'],
        'delimiter': '|'
    },

    'category': {
        'filename': 'category_pipe.txt',
        'col_names': ['category_id', 'category_group', 
                            'category_name', 'category_desc'],
        'delimiter': '|'
    }
}

def arg_parse():
    parser = ArgumentParser()
    parser.add_argument("--s3-bucket-arn", 
                        default='s3://tickit-data-1', 
                        help="for loading data to tables in Data source(db)")

    parser.add_argument('--username', 
                        default='admin',
                        help="Username for the database")

    parser.add_argument('--password', 
                        default='password',
                        help="Password for the database")

    parser.add_argument('--host', 
                        default='0.0.0.0',
                        help="Either endpoint or ip add of database")

    parser.add_argument('--database-name', 
                        default='tickit',
                        help="Database Name")

    args = parser.parse_args()
    return args 


def load_data_into_db(dataframe, table_name):
    try:
        db_url_str = f'mysql+pymysql://{args.username}:{args.password}@{args.host}/{args.database_name}'
        print(db_url_str)
        engine = create_engine(db_url_str)

        with engine.begin() as conn:
            # Invoke DataFrame method to_sql() to
            # create the table 'largest_cities' and
            # insert all the DataFrame rows into it
            dataframe.to_sql(
                name=table_name, # database table
                con=conn, # database connection
                index=False # Don't save index
            )

    except Exception as err:
        raise 


def main(args):
    for table_name, data in DATA_DETAILS.items():
        # load the data from s3 as df 
        s3_url = args.s3_bucket_arn + '/' + data.get('filename')
        df = pd.read_csv(s3_url, delimiter=data.get('delimiter'),  names=data.get('col_names'))
        
        # load data into database tables
        load_data_into_db(df, table_name)
        

if __name__ == '__main__':
    args = arg_parse()
    main(args)

