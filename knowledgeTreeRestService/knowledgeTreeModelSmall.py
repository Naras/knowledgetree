from peewee import *
import json
# import logging
# import socket
# logging.basicConfig(filename='knowledgeTreeDBJournal.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

def get_username():
    dbcredentials = json.load(open("db_credentials.txt"))
    if 'user' in dbcredentials:
        return dbcredentials['user']
    return None
def get_password():
    dbcredentials = json.load(open("db_credentials.txt"))
    if 'user' in dbcredentials:
        return dbcredentials['password']
    return None
def get_dbhost():
    try:
        # socket.gethostbyname(socket.gethostname())
        hosturl = file('database_url.txt').read()
        return hosturl
    except:
        return None

database_url = get_dbhost()
if database_url==None:
    # logging.debug('local access.db user:'+ get_username()+' db password:' + get_password());
    database = MySQLDatabase('knowledgetree', **{'user': get_username(), 'password': get_password()})
else:
    # logging.debug('remote access.db user:'+ get_username()+' db password:' + get_password());
    database = MySQLDatabase('knowledgetree', host=database_url, port=3306, user = get_username(), password=get_password())

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Person(BaseModel):
    first = CharField(db_column='First')
    initials = CharField(db_column='Initials', null=True)
    last = CharField(db_column='Last', null=True)
    middle = CharField(db_column='Middle', null=True)
    nick = CharField(db_column='Nick', null=True)
    other = CharField(db_column='Other', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'person'

class Language(BaseModel):
    name = CharField(db_column='Name', null=True)
    unicodeblock = IntegerField(db_column='UnicodeBlock', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'language'

class Script(BaseModel):
    name = CharField(db_column='Name', null=True)
    unicodeblock = IntegerField(db_column='UnicodeBlock', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'script'

class Subject(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name')
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'subject'

class SubjectSubjectRelation(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'subject_subject_relation'

class SubjectRelatestoSubject(BaseModel):
    subject1 = ForeignKeyField(db_column='Subject1', rel_model=Subject, to_field='id')
    subject2 = ForeignKeyField(db_column='Subject2', rel_model=Subject, related_name='subject_subject2_set', to_field='id')
    relation = ForeignKeyField(db_column='relation_id', null=True, rel_model=SubjectSubjectRelation, to_field='id')
    sortorder = IntegerField(null=True)

    class Meta:
        db_table = 'subject_relatesto_subject'
        primary_key = CompositeKey('subject1', 'subject2')

