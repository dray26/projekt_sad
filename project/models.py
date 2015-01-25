#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw

myDB = pw.MySQLDatabase("projektdb", host="localhost", port=3306, user="root", passwd="root")

class MySQLModel(pw.Model):
    class Meta:
        database = myDB

class Rss(MySQLModel):
   # idrssFeed = pw.IntegerField(primary_key=True)
   name = pw.CharField()
   link = pw.CharField()


class Cities(MySQLModel):
    # idcities = pw.IntegerField(primary_key=True)
    name = pw.CharField()


class Judgment_Data(MySQLModel):
    # idjudgment_data = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    address = pw.CharField()
    faculty = pw.CharField()


class MetaData(MySQLModel):
    # idmetadata = pw.IntegerField(primary_key=True)
    links = pw.CharField()
    dateCreate = pw.CharField()
    rss = pw.ForeignKeyField(Rss)



class Judgment(MySQLModel):
    # idjudgment = pw.IntegerField(primary_key=True)
    title = pw.CharField()
    chairman = pw.CharField()
    date_of_judgment = pw.CharField()
    date_publication = pw.CharField()
    signature = pw.CharField()
    judges = pw.CharField()
    recorder = pw.CharField()
    legal_basis = pw.CharField()
    judgmentdata = pw.ForeignKeyField(Judgment_Data)
    metadata = pw.ForeignKeyField(MetaData)
    cities = pw.ForeignKeyField(Cities)

class Statistic(MySQLModel):
    # idstatistic = pw.IntegerField(primary_key=True)
    prices = pw.IntegerField()
    judgmentdata = pw.ForeignKeyField(Judgment)

class Key(MySQLModel):
    # idkey = pw.IntegerField(primary_key=True)
    typ = pw.CharField()
    value = pw.CharField()
    judgment = pw.ForeignKeyField(Judgment)






# when you're ready to start querying, remember to connect
myDB.connect()

