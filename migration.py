import sqlite3

migration_file='test1.sqlite'

conn = sqlite3.connect(migration_file)

cursor = conn.cursor()

cursor.execute('CREATE TABLE "stuff" ("Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"Data"	TEXT NOT NULL,"Type"	INTEGER NOT NULL);') # create first table

cursor.execute('CREATE TABLE "subscriptions" ("Id"	INTEGER PRIMARY KEY AUTOINCREMENT,"Type"	INTEGER NOT NULL,"ChatId"	TEXT NOT NULL,"Data"	TEXT);') #second

cursor.execute('CREATE TABLE "users" ("Id"	INTEGER NOT NULL,"TelegramChatId"	TEXT NOT NULL,"Password"	TEXT,"Username"	TEXT,"TelegramId"	TEXT,PRIMARY KEY("Id"));') #third for users

conn.close()