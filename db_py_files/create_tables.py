from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

import psycopg2
from psycopg2 import sql, Error

from exceptions import NotSupportedError
from sql_commands import get_table_commands

from argparse import ArgumentParser


def arg_parse():
    parser = ArgumentParser()

    parser.add_argument('--username', 
                        default='admin',
                        help="Username for the database", 
                        type=str)

    parser.add_argument('--password', 
                        default='password',
                        help="Password for the database", 
                        type=str)

    parser.add_argument('--host', 
                        default='0.0.0.0',
                        help="Either endpoint or ip add of database", 
                        type=str)

    parser.add_argument('--port', 
                        default=3306,
                        help="Port number of DBMs", 
                        type=int)
    
    parser.add_argument('--tables-to-include', 
                        default=['category', 'event', 'venue'],
                        help="Port number of DBMs", 
                        type=list)

    parser.add_argument('--rdbms-type', 
                        default="mysql",
                        choices=["mysql", "postgres"],
                        help="Either Mysql or postgres is supported", 
                        type=str)

    parser.add_argument('--database-name', 
                        default="postgres",
                        help="Need for postgres client", 
                        type=str)

    args = parser.parse_args()
    return args


def get_db_object(args):
    try:
        if args.rdbms_type == "mysql":
            connection = mysql.connector.connect(user=args.username, 
                                            password=args.password, 
                                            host=args.host, 
                                            port=args.port)

            cursor = connection.cursor()

            return connection, cursor

        elif args.rdbms_type == "postgres":
            connection = psycopg2.connect(user=args.username, 
                                        password=args.password, 
                                        host=args.host, 
                                        port=args.port, 
                                        database=args.database_name)

            cursor = connection.cursor()

            return connection, cursor


    except Exception as err:
        print(err)
        raise


def create_table(cursor, connection, args, table_name, table_description):
    try:
        if args.rdbms_type == "mysql":
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)

        elif args.rdbms_type == "postgres":
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)

            connection.commit()

        else:
            raise NotSupportedError("Provided RDBMS is not supported.")

    except NotsupportedError as err:
        print(err)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(err.msg)

    except Error as err:
        if e.pgcode == '42P07':  # PostgreSQL error code for table already exists
            print("Table already exists.")

        else:
            print(err.msg)

        connection.rollback()

    else:
        print("OK")


# create database and tables
def main(args):
    TABLES = get_table_commands(args.rdbms_type)
    db_name = args.database_name
    try:
        connection, cursor = get_db_object(args)

        if args.rdbms_type == "mysql":
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.execute("USE {}".format(db_name))

        for table_name in args.tables_to_include:
            table_description = TABLES[table_name]
            
            create_table(cursor, connection, args, table_name, table_description)

        cursor.close()  
        connection.close()

    except Exception as err:
        print(err)


if __name__ == '__main__':
    args = arg_parse()
    main(args)