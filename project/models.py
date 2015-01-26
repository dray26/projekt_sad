#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw

myDB = pw.MySQLDatabase("projektdb", host="localhost", port=3306, user="root", passwd="root")

class MySQLModel(pw.Model):
    class Meta:
        database = myDB



class Cities(MySQLModel):
    # idcities = pw.IntegerField(primary_key=True)
    name = pw.CharField()


class Rss(MySQLModel):
   idrssFeed = pw.IntegerField(primary_key=True)
   name = pw.CharField()
   link = pw.CharField()
   cities = pw.ForeignKeyField(Cities)

class MetaData(MySQLModel):
    # idmetadata = pw.IntegerField(primary_key=True)
    links = pw.CharField()
    rss = pw.ForeignKeyField(Rss)



class Judgment(MySQLModel):
    # idjudgment = pw.IntegerField(primary_key=True)
    title = pw.CharField()
    date_of_judgment = pw.CharField()
    date_publication = pw.CharField()
    signature = pw.CharField()
    judgement_name = pw.CharField()
    judges = pw.CharField()
    faculty = pw.CharField()
    chairman = pw.CharField()
    recorder = pw.CharField()
    legal_basis = pw.CharField()
    metadata = pw.ForeignKeyField(MetaData)
    cities = pw.ForeignKeyField(Cities)

class Key(MySQLModel):
    # idkey = pw.IntegerField(primary_key=True)
    typ = pw.CharField()
    value = pw.CharField()
    judgment = pw.ForeignKeyField(Judgment)






# when you're ready to start querying, remember to connect
myDB.connect()

