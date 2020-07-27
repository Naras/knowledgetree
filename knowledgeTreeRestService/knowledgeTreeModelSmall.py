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
        hosturlfile = open('database_url.txt')
        hosturl = hosturlfile.read()
        hosturlfile.close()
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

class Subject(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name')
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'subject'

# class Orphan(BaseModel):
#     description = CharField(db_column='Description', null=True)
#     name = CharField(db_column='Name')
#     id = CharField(primary_key=True)
#
#     class Meta:
#         db_table = 'orphan'

class SubjectSubjectRelation(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'subject_subject_relation'

class SubjectRelatestoSubject(BaseModel):
    relation = ForeignKeyField(column_name='Relation', field='id', model=SubjectSubjectRelation, null=True)
    sortorder = IntegerField(column_name='Sortorder', null=True)
    subject1 = ForeignKeyField(column_name='Subject1', field='id', model=Subject)
    subject2 = ForeignKeyField(backref='subject_subject2_set', column_name='Subject2', field='id', model=Subject)

    class Meta:
        table_name = 'subject_relatesto_subject'
        indexes = (
            (('subject1', 'subject2'), True),
        )
        primary_key = CompositeKey('subject1', 'subject2')

class Work(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'work'

class WorkWorkRelation(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'work_work_relation'

class WorkRelatestoWork(BaseModel):
    relation = ForeignKeyField(column_name='Relation', field='id', model=WorkWorkRelation, null=True)
    sortorder = IntegerField(column_name='Sortorder', null=True)
    work1 = ForeignKeyField(column_name='Work1', field='id', model=Work)
    work2 = ForeignKeyField(backref='work_work2_set', column_name='Work2', field='id', model=Work)

    class Meta:
        table_name = 'work_relatesto_work'
        indexes = (
            (('work1', 'work2'), True),
        )
        primary_key = CompositeKey('work1', 'work2')

class WorkSubjectRelation(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'work_subject_relation'

class SubjectHasWork(BaseModel):
    relation = ForeignKeyField(column_name='Relation', field='id', model=WorkSubjectRelation)
    subject = ForeignKeyField(column_name='Subject', field='id', model=Subject)
    work = ForeignKeyField(column_name='Work', field='id', model=Work)

    class Meta:
        table_name = 'subject_has_work'
        indexes = (
            (('subject', 'work', 'relation'), True),
        )
        primary_key = CompositeKey('relation', 'subject', 'work')

class Person(BaseModel):
    biography = CharField(column_name='Biography', null=True)
    birth = DateField(column_name='Birth', null=True)
    death = DateField(column_name='Death', null=True)
    first = CharField(column_name='First', null=True)
    initials = CharField(column_name='Initials', null=True)
    last = CharField(column_name='Last', null=True)
    living = IntegerField(column_name='Living', constraints=[SQL("DEFAULT 1")], null=True)
    middle = CharField(column_name='Middle', null=True)
    nick = CharField(column_name='Nick', null=True)
    other = CharField(column_name='Other', null=True)
    period = CharField(column_name='Period', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'person'

class PersonWorkRelation(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'person_work_relation'

class PersonHasWork(BaseModel):
    person = ForeignKeyField(column_name='Person', field='id', model=Person)
    relation = ForeignKeyField(column_name='Relation', field='id', model=PersonWorkRelation)
    work = ForeignKeyField(column_name='Work', field='id', model=Work)

    class Meta:
        table_name = 'person_has_work'
        indexes = (
            (('person', 'work', 'relation'), True),
        )
        primary_key = CompositeKey('person', 'relation', 'work')

class PersonPersonRelation(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'person_person_relation'

class PersonRelatestoPerson(BaseModel):
    person1 = ForeignKeyField(column_name='person1', field='id', model=Person)
    person2 = ForeignKeyField(backref='person_person2_set', column_name='person2', field='id', model=Person)
    relation = ForeignKeyField(column_name='relation', field='id', model=PersonPersonRelation)

    class Meta:
        table_name = 'person_relatesto_person'
        indexes = (
            (('person1', 'person2', 'relation'), True),
        )
        primary_key = CompositeKey('person1', 'person2', 'relation')




