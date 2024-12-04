#!/bin/bash
mysql --execute="CREATE DATABASE IF NOT EXISTS $mysql_db_name;"
mysql --execute="CREATE USER $mysql_user@$mysql_ip IDENTIFIED BY '$mysql_password';"
mysql --execute="FLUSH PRIVILEGES;"
mysql --execute="GRANT ALL PRIVILEGES ON $mysql_db_name.* TO $mysql_user@$mysql_ip WITH GRANT OPTION;"
