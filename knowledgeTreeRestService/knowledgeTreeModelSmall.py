from peewee import *

database = MySQLDatabase('knowledgetree', **{'user': 'root', 'password': 'root123'})
# database = MySQLDatabase('knowledgetree', host='freedbinstance.cmi50o02mh1u.us-west-2.rds.amazonaws.com', port=3306, user = 'narasmg', password='Master01')

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
    relations = ForeignKeyField(db_column='Relations_id', null=True, rel_model=SubjectSubjectRelation, related_name='subject_subject_relation_relations_set', to_field='id')
    subject1 = ForeignKeyField(db_column='Subject1', rel_model=Subject, related_name='subject_subject1_set', to_field='id')
    subject2 = ForeignKeyField(db_column='Subject2', rel_model=Subject, related_name='subject_subject2_set', to_field='id')

    class Meta:
        db_table = 'subject_relatesto_subject'
        primary_key = CompositeKey('subject1', 'subject2')