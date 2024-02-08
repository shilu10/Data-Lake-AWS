from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode


USERNAME = 'admin'
PASSWORD = 'shilu1234'
HOST = 'database-1.c16mckgi21hz.ap-southeast-2.rds.amazonaws.com'
DB_NAME = 'tickit'
TABLES = {}

connection = mysql.connector.connect(user=USERNAME, 
                                    password=PASSWORD, 
                                    host=HOST)

cursor = connection.cursor()


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
    "  `start_time` DATE,"

    "  PRIMARY KEY (`event_id`)"
    ") ENGINE=InnoDB")

TABLES['venue'] = (
    "CREATE TABLE `venue` ("
    "  `venue_id` SMALLINT NOT NULL,"
    "  `venue_name` VARCHAR(100),"
    "  `venue_city` VARCHAR(30),"
    "  `venue_state` INT,"
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
    "  `price_paid` TEXT,"
    "  `commission` TEXT,"
    "  `sale_time` DATE,"

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

    "  PRIMARY KEY (`dateid`)"
    ") ENGINE=InnoDB")

TABLES['listing'] = (
    "CREATE TABLE `listing` ("
    "  `list_id` INT NOT NULL,"
    "  `seller_id` INT,"
    "  `date_id` SMALLINT,"
    "  `num_tickets` SMALLINT,"
    "  `price_perticket` TEXT,"
    "  `total_price` TEXT,"
    "  `list_time` TIMESTAMP,"

    "  PRIMARY KEY (`list_id`)"
    ") ENGINE=InnoDB")

TABLES['listing'] = (
    "CREATE TABLE `listing` ("
    "  `list_id` INT NOT NULL,"
    "  `seller_id` INT,"
    "  `date_id` SMALLINT,"
    "  `num_tickets` SMALLINT,"
    "  `price_perticket` TEXT,"
    "  `total_price` TEXT,"
    "  `list_time` TIMESTAMP,"

    "  PRIMARY KEY (`list_id`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        connection.database = DB_NAME
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