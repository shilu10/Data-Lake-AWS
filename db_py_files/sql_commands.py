from exceptions import NotSupportedError


MYSQL_TABLES = {}

MYSQL_TABLES['category'] = (
    "CREATE TABLE `category` ("
    "  `category_id` SMALLINT NOT NULL,"
    "  `category_group` VARCHAR(10),"
    "  `category_name` VARCHAR(10),"
    "  `category_desc` VARCHAR(50),"
    "  PRIMARY KEY (`category_id`)"
    ") ENGINE=InnoDB")

MYSQL_TABLES['event'] = (
    "CREATE TABLE `event` ("
    "  `event_id` INT NOT NULL,"
    "  `venue_id` SMALLINT NOT NULL,"
    "  `cat_id` SMALLINT NOT NULL,"
    "  `date_id` SMALLINT NOT NULL,"
    "  `event_name` VARCHAR(200),"
    "  `start_time` TIMESTAMP,"

    "  PRIMARY KEY (`event_id`)"
    ") ENGINE=InnoDB")

MYSQL_TABLES['venue'] = (
    "CREATE TABLE `venue` ("
    "  `venue_id` SMALLINT NOT NULL,"
    "  `venue_name` VARCHAR(100),"
    "  `venue_city` VARCHAR(30),"
    "  `venue_state` CHAR(20),"
    "  `venue_seats` INT,"
    "  PRIMARY KEY (`venue_id`)"
    ") ENGINE=InnoDB")


MYSQL_TABLES['sales'] = (
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

MYSQL_TABLES['date'] = (
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

MYSQL_TABLES['listing'] = (
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

MYSQL_TABLES['user'] = (
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


POSTGRES_TABLES = {}

POSTGRES_TABLES['category'] = (
    "CREATE TABLE category ("
    "  category_id SMALLSERIAL PRIMARY KEY,"
    "  category_group VARCHAR(10),"
    "  category_name VARCHAR(10),"
    "  category_desc VARCHAR(50)"
    ");"
)

POSTGRES_TABLES['event'] = (
    "CREATE TABLE event ("
    "  event_id SERIAL PRIMARY KEY,"
    "  venue_id SMALLINT NOT NULL,"
    "  cat_id SMALLINT NOT NULL,"
    "  date_id SMALLINT NOT NULL,"
    "  event_name VARCHAR(200),"
    "  start_time TIMESTAMP"
    ");"
)

POSTGRES_TABLES['venue'] = (
    "CREATE TABLE venue ("
    "  venue_id SMALLSERIAL PRIMARY KEY,"
    "  venue_name VARCHAR(100),"
    "  venue_city VARCHAR(30),"
    "  venue_state CHAR(20),"
    "  venue_seats INT"
    ");"
)

POSTGRES_TABLES['sales'] = (
    "CREATE TABLE sales ("
    "  sales_id SERIAL PRIMARY KEY,"
    "  list_id INT,"
    "  seller_id INT,"
    "  buyer_id INT,"
    "  event_id INT,"
    "  date_id SMALLINT,"
    "  qty_sold SMALLINT,"
    "  price_paid NUMERIC,"
    "  commission NUMERIC,"
    "  sale_time TIMESTAMP"
    ");"
)

POSTGRES_TABLES['date'] = (
    "CREATE TABLE date ("
    "  date_id SMALLSERIAL PRIMARY KEY,"
    "  cal_date DATE,"
    "  day CHAR(3),"
    "  week SMALLINT,"
    "  month CHAR(3),"
    "  qtr CHAR(3),"
    "  year SMALLINT,"
    "  holiday BOOL"
    ");"
)

POSTGRES_TABLES['listing'] = (
    "CREATE TABLE listing ("
    "  list_id SERIAL PRIMARY KEY,"
    "  seller_id INT NOT NULL,"
    "  event_id INT NOT NULL,"
    "  date_id SMALLINT NOT NULL,"
    "  num_tickets SMALLINT,"
    "  price_perticket NUMERIC,"
    "  total_price NUMERIC,"
    "  list_time TIMESTAMP"
    ");"
)

POSTGRES_TABLES['user'] = (
    "CREATE TABLE user ("
    "  user_id SERIAL PRIMARY KEY,"
    "  user_name CHAR(8),"
    "  first_name VARCHAR(30),"
    "  last_name VARCHAR(30),"
    "  city VARCHAR(30),"
    "  state CHAR(2),"
    "  email VARCHAR(100),"
    "  phone CHAR(14),"
    "  like_sports BOOL,"
    "  like_theatre BOOL,"
    "  like_concerts BOOL,"
    "  like_jazz BOOL,"
    "  like_classical BOOL,"
    "  like_opera BOOL,"
    "  like_rock BOOL,"
    "  like_vegas BOOL,"
    "  like_broadway BOOL,"
    "  like_musicals BOOL"
    ");"
)


def get_table_commands(rdbms_type):
    try: 
        if rdbms_type == "mysql":
            return MYSQL_TABLES

        elif rdbms_type == "postgres":
            return POSTGRES_TABLES

        else: 
            raise NotSupportedError("Provided RDBMS type not supported")


    except NotSupportedError as err:
        return err 