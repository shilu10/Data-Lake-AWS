from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

from argparse import ArgumentParser


USERNAME = 'admin'
PASSWORD = 'shilu1234'
HOST = 'database-1.c16mckgi21hz.ap-southeast-2.rds.amazonaws.com'
DB_NAME = 'tickit'

TABLES = {}

TABLES['category'] = (
    "CREATE TABLE `category` ("
    "  `category_id` SMALLINT NOT NULL,"
    "  `category_group` VARCHAR(10),"
    "  `category_name` VARCHAR(10),"
    "  `category_desc` VARCHAR(50),"
    "  PRIMARY KEY (`category_id`)"
    ") ENGINE=InnoDB")

TABLES['event'] = (
    "CREATE TABLE `event` ("
    "  `event_id` INT NOT NULL,"
    "  `venue_id` SMALLINT NOT NULL,"
    "  `cat_id` SMALLINT NOT NULL,"
    "  `date_id` SMALLINT NOT NULL,"
    "  `event_name` VARCHAR(200),"
    "  `start_time` TIMESTAMP,"

    "  PRIMARY KEY (`event_id`)"
    ") ENGINE=InnoDB")

TABLES['venue'] = (
    "CREATE TABLE `venue` ("
    "  `venue_id` SMALLINT NOT NULL,"
    "  `venue_name` VARCHAR(100),"
    "  `venue_city` VARCHAR(30),"
    "  `venue_state` CHAR(20),"
    "  `venue_seats` INT,"
    "  PRIMARY KEY (`venue_id`)"
    ") ENGINE=InnoDB")


TABLES['sales'] = (
    "CREATE TABLE `sales` ("
    "  `sales_id` INT NOT NULL,"
    "  `list_id` INT,"
    "  `seller_id` INT,"
    "  `buyer_id` INT,"
    "  `event_id` INT,"
    "  `date_id` SMALLINT,"
    "  `qty_sold` SMALLINT,"
    "  `price_paid` NUMERIC,"
    "  `commission` NUMERIC,"
    "  `sale_time` TIMESTAMP,"

    "  PRIMARY KEY (`sales_id`)"
    ") ENGINE=InnoDB")

TABLES['date'] = (
    "  CREATE TABLE `date` ("
    "  `date_id` SMALLINT NOT NULL,"
    "  `cal_date` DATE,"
    "  `day` CHAR(3),"
    "  `week` SMALLINT,"
    "  `month` CHAR(3),"
    "  `qtr` CHAR(3),"
    "  `year` SMALLINT,"
    "  `holiday` BOOL,"

    "  PRIMARY KEY (`date_id`)"
    ") ENGINE=InnoDB")

TABLES['listing'] = (
    "CREATE TABLE `listing` ("
    "  `list_id` INT NOT NULL,"
    "  `seller_id` INT NOT NULL,"
    "  `event_id` INT NOT NULL,"
    "  `date_id` SMALLINT NOT NULL,"
    "  `num_tickets` SMALLINT,"
    "  `price_perticket` NUMERIC,"
    "  `total_price` NUMERIC,"
    "  `list_time` TIMESTAMP,"

    "  PRIMARY KEY (`list_id`)"
    ") ENGINE=InnoDB")

TABLES['user'] = (
    "CREATE TABLE `user` ("
    "  `user_id` INT NOT NULL,"
    "  `user_name` CHAR(8),"
    "  `first_name` VARCHAR(30),"
    "  `last_name` VARCHAR(30),"
    "  `city` VARCHAR(30),"
    "  `state` CHAR(2),"
    "  `email` VARCHAR(100),"
    "  `phone` CHAR(14),"
    "  `like_sports` BOOL,"
    "  `like_theatre` BOOL,"
    "  `like_concerts` BOOL,"
    "  `like_jazz` BOOL,"
    "  `like_classical` BOOL,"
    "  `like_opera` BOOL,"
    "  `like_rock` BOOL,"
    "  `like_vegas` BOOL,"
    "  `like_broadway` BOOL,"
    "  `like_musicals` BOOL,"

    "  PRIMARY KEY (`user_id`)"
    ") ENGINE=InnoDB")


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

    parser.add_argument('--database-name', 
                        default='tickit',
                        help="Database Name", 
                        type=str)

    parser.add_argument('--port', 
                        default=3306,
                        help="Port number of DBMs", 
                        type=int)

    args = parser.parse_args()
    return args


def get_db_object(args):
    connection = mysql.connector.connect(user=args.username, 
                                    password=args.password, 
                                    host=args.host, 
                                    port=args.port)

    cursor = connection.cursor()

    return connection, cursor


def create_database(cursor, name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


# create database and tables
def main(args):
    db_name = args.database_name
    try:
        connection, cursor = get_db_object(args)
        cursor.execute("USE {}".format(db_name))
        
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, db_name)
            print("Database {} created successfully.".format(db_name))
            connection.database = db_name
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()  
    connection.close()


if __name__ == '__main__':
    args = arg_parse()
    main(args)