#!/usr/bin/python

###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Rahul Kumar
# Modified by : Kevin Martinez
# Website: http://tecadmin.net
# Created date: Dec 03, 2013
# Last modified: Nov 05, 2020 
# Tested with : Python 3.8.5
# Script Revision: 1.6
#
##########################################################

# Import required python libraries

import os
import time
import datetime
import pipes
from progress.bar import Bar


# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.

DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = '_mysql_user_password_'
DB_NAME = 'dbnameslist.txt'
#DB_NAME = 'db_name_to_backup'
BACKUP_PATH =r"D:\Backup"

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = "{}\{}".format(BACKUP_PATH,DATETIME)


# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
     os.makedirs(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print ("checking for databases names file.")
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print ("Databases file found...")
    print ("Starting backup of all dbs listed in file{}".format(DB_NAME))
else:
    print ("Databases file not found...")
    print ("Starting backup of database{}".format(DB_NAME))
    multi = 0

# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   bar = Bar('Processing', max=flength)
   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = 'mysqldump -h {} -u {}  --password={} {}  > {}\{}.sql'.format(DB_HOST,DB_USER,DB_USER_PASSWORD,db,TODAYBACKUPPATH,db)
       os.system(dumpcmd)
       gzipcmd = "gzip {}/{}.sql".format(TODAYBACKUPPATH,db)
       os.system(gzipcmd)
       bar.next()
       p = p + 1
   dbfile.close()
   bar.finish()
else:
   db = DB_NAME
   dumpcmd = 'mysqldump -h {} -u {}  --password={} {}  > {}\{}.sql'.format(DB_HOST,DB_USER,DB_USER_PASSWORD,db,TODAYBACKUPPATH,db)
   os.system(dumpcmd)
   gzipcmd = "gzip {}/{}.sql".format(TODAYBACKUPPATH,db)
   os.system(gzipcmd)
 

print ("")
print ("Backup script completed")
print ("Your backups have been created in {} directory".format(TODAYBACKUPPATH))
