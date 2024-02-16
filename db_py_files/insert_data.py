from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine

import psycopg2

import pandas as pd 
import numpy as np 

import boto3
from argparse import ArgumentParser

from exceptions import NotSupportedError


DATA_DETAILS = {
    'event': {
        'filename': 'allevents_pipe.txt',
        'col_names': ['event_id', 'venue_id', 'cat_id',
                             'date_id', 'event_name', 'start_time'],
        'delimiter': '|', 
        'dtypes': {
            'event_id': int,
            'venue_id': int,
            'cat_id': int,
            'date_id': int,
        }
    },

    'category': {
        'filename': 'category_pipe.txt',
        'col_names': ['category_id', 'category_group', 
                            'category_name', 'category_desc'],
        'delimiter': '|',
        'dtypes': {
            'category_id': int,
        }
    },

    'venue': {
        'filename': 'venue_pipe.txt',
        'col_names': ['venue_id', 'venue_name', 
                            'venue_city', 'venue_state', 'venue_seats'],
        'delimiter': '|',
        'dtypes': {
            'venue_id': int,
        }
    },

    'sales': {
        'filename': 'sales_tab.txt',
        'col_names': ['sales_id', 'list_id', 'seller_id', 
                            'buyer_id', 'event_id', 'date_id',
                            'qty_sold', 'price_paid', 'commission', 'sale_time'],
        'delimiter': '\t',
        'dtypes': {
            'sales_id': int,
            'list_id': int,
            'seller_id': int,
            'buyer_id': int,
            'event_id': int,
            'date_id': int,
            'qty_sold': int,
        }
    },

    'date': {
        'filename': 'date2008_pipe.txt',
        'col_names': ['date_id', 'cal_date', 'day',
                            'week', 'month', 'qtr', 'year', 'holiday'],
        'delimiter': '|', 
        'dtypes': {
            'date_id': int,
            'week': int,
            'year': int,
        }
    },

    'listing': {
        'filename': 'listings_pipe.txt',
        'col_names': ['list_id', 'seller_id', 'event_id',
                            'date_id', 'num_tickets', 'price_perticket', 
                            'total_price', 'list_time'],
        'delimiter': '|',
        'dtypes': {
            'list_id': int,
            'seller_id': int,
            'event_id': int,
            'date_id': int,
            'num_tickets': int,
        }
    },

    'user': {
        'filename': 'allusers_pipe.txt',
        'col_names': ['user_id', 'user_name', 'first_name',
                            'last_name', 'city', 'state', 'email',
                            'phone', 'like_sports', 'like_theatre', 
                            'like_concerts', 'like_jazz', 'like_classical', 
                            'like_opera', 'like_rock', 'like_vegas', 'like_broadway',
                            'like_musicals'],
        'delimiter': '|',
        'dtypes': {
            'user_id': int,
        }
    },

}

def arg_parse():
    parser = ArgumentParser()
    parser.add_argument("--s3-bucket-arn", 
                        default='s3://tickit-data-1', 
                        help="for loading data to tables in Data source(db)", 
                        type=str)

    parser.add_argument('--username', 
                        default='admin',
                        help="Username for the database", 
                        type=str)

    parser.add_argument('--password', 
                        default='password',
                        help="Password for the database", type=str)

    parser.add_argument('--host', 
                        default='0.0.0.0',
                        help="Either endpoint or ip add of database", 
                        type=str)

    parser.add_argument('--database-name', 
                        default='tickit',
                        help="Database Name", 
                        type=str)

    parser.add_argument('--tables-to-include', 
                        default=['category', 'event', 'venue'],
                        help="Port number of DBMs", 
                        type=list)

    parser.add_argument('--rdbms-type', 
                        default="mysql",
                        choices=["mysql", "postgres"],
                        help="Either Mysql or postgres is supported", 
                        type=str)

    parser.add_argument('--start-index', 
                        default=0,
                        help="It defines at which index the dataframe starts from.", 
                        type=int)

    parser.add_argument('--end-index', 
                        default=10,
                        help="It defines at which index the dataframe ends at. when -1 is given it ends last index of df", 
                        type=int)

    args = parser.parse_args()
    return args 


def __create_engine(args):
    try:
        if args.rdbms_type == "mysql":
            print("in")
            db_url_str = f'mysql+pymysql://{args.username}:{args.password}@{args.host}/{args.database_name}'
            engine = create_engine(db_url_str)

            return engine 
        
        elif args.rdbms_type == "postgres":
            db_url_str = f'postgresql+psycopg2://{args.username}:{args.password}@{args.host}/{args.database_name}'
            engine = create_engine(db_url_str)

            return engine 

        else: 
            raise NotSupportedError("Provided RDBMS is not supported")

    except Exception as err:
        print(err)


def load_data_into_db(args, dataframe, table_name):
    try:
        
        engine = __create_engine(args)

        with engine.begin() as conn:
            # Invoke DataFrame method to_sql() to
            # create the table 'largest_cities' and
            # insert all the DataFrame rows into it
            dataframe.to_sql(
                name=table_name, # database table
                con=conn, # database connection
                index=False, # Don't save index, 
                if_exists='append', 
                chunksize=1000
            )

        print(f"Inserted data into the {table_name} table: OK")

    except Exception as err:
        print(f"Inserted data into the {table_name} table: Failed")
        raise 


def main(args):
    for table_name in args.tables_to_include:
        data = DATA_DETAILS[table_name]

        # load the data from s3 as df 
        s3_url = args.s3_bucket_arn + '/' + data.get('filename')
        df = pd.read_csv(s3_url, 
                        delimiter=data.get('delimiter'),
                        names=data.get('col_names'), 
                        dtype=data.get('dtypes'))

        if table_name == "venue":
            #df['venue_seats'][df['venue_seats'] == '\\N'] = None
            df.loc[df['venue_seats'] == '\\N', 'venue_seats'] = None

        start_index = args.start_index
        end_index = args.end_index 
        if end_index == -1:
            df = df.iloc[start_index: ]

        else:
            df = df.iloc[start_index: end_index]
        
        # load data into database tables
        load_data_into_db(args, df, table_name)
        

if __name__ == '__main__':
    args = arg_parse()
    main(args)

