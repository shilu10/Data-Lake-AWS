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
        'delimiter': '|', 
        'dtypes': {
            'event_id': int,
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
            'venue_seats': int,
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

    args = parser.parse_args()
    return args 


def load_data_into_db(dataframe, table_name):
    try:
        db_url_str = f'mysql+pymysql://{args.username}:{args.password}@{args.host}/{args.database_name}'
        engine = create_engine(db_url_str)

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
    for table_name, data in DATA_DETAILS.items():
        # load the data from s3 as df 
        s3_url = args.s3_bucket_arn + '/' + data.get('filename')
        df = pd.read_csv(s3_url, 
                        delimiter=data.get('delimiter'),
                        names=data.get('col_names'), 
                        dtype=data.get('dtypes'))
        
        # load data into database tables
        load_data_into_db(df, table_name)
        

if __name__ == '__main__':
    args = arg_parse()
    main(args)

