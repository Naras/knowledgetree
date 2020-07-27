from peewee import *

database = MySQLDatabase('knowledgetree', **{'charset': 'utf8', 'use_unicode': True, 'port': 3306, 'user': 'root', 'password': 'root123'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Country(BaseModel):
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'country'

class State(BaseModel):
    country = ForeignKeyField(column_name='Country_id', field='id', model=Country)
    name = CharField(column_name='Name', null=True)
    id = CharField()

    class Meta:
        table_name = 'state'
        indexes = (
            (('id', 'country'), True),
        )
        primary_key = CompositeKey('country', 'id')

class City(BaseModel):
    country = ForeignKeyField(column_name='Country_id', field='country', model=State)
    name = CharField(column_name='Name', null=True)
    state = ForeignKeyField(backref='state_state_set', column_name='State_id', field='id', model=State)
    id = CharField()

    class Meta:
        table_name = 'city'
        indexes = (
            (('id', 'state', 'country'), True),
            (('state', 'country'), False),
        )
        primary_key = CompositeKey('country', 'id', 'state')

class District(BaseModel):
    country = ForeignKeyField(column_name='Country_id', field='country', model=State)
    name = CharField(column_name='Name', null=True)
    state = ForeignKeyField(backref='state_state_set', column_name='State_id', field='id', model=State)
    id = CharField()

    class Meta:
        table_name = 'district'
        indexes = (
            (('id', 'state', 'country'), True),
            (('state', 'country'), False),
        )
        primary_key = CompositeKey('country', 'id', 'state')

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

class Address(BaseModel):
    area = CharField(column_name='Area', null=True)
    city_country = ForeignKeyField(column_name='City_Country_id', field='country', model=City, null=True)
    city_state = ForeignKeyField(backref='city_city_state_set', column_name='City_State_id', field='state', model=City, null=True)
    city = ForeignKeyField(backref='city_city_set', column_name='City_id', field='id', model=City, null=True)
    district_country = ForeignKeyField(column_name='District_Country_id', field='country', model=District, null=True)
    district_state = ForeignKeyField(backref='district_district_state_set', column_name='District_State_id', field='state', model=District, null=True)
    district = ForeignKeyField(backref='district_district_set', column_name='District_id', field='id', model=District, null=True)
    housenumber = CharField(column_name='HouseNumber', null=True)
    person = ForeignKeyField(column_name='Person', field='id', model=Person, null=True)
    street = CharField(column_name='Street', null=True)
    value = CharField(column_name='Value', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'address'
        indexes = (
            (('city', 'city_state', 'city_country'), False),
            (('district', 'district_state', 'district_country'), False),
        )

class Affiliation(BaseModel):
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'affiliation'

class Language(BaseModel):
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'language'

class PersonHasAffiliation(BaseModel):
    affiliation = ForeignKeyField(column_name='affiliation', field='id', model=Affiliation)
    person = ForeignKeyField(column_name='person', field='id', model=Person)

    class Meta:
        table_name = 'person_has_affiliation'
        indexes = (
            (('person', 'affiliation'), True),
        )
        primary_key = CompositeKey('affiliation', 'person')

class Role(BaseModel):
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'role'

class PersonHasRole(BaseModel):
    person = ForeignKeyField(column_name='person', field='id', model=Person)
    role = ForeignKeyField(column_name='role', field='id', model=Role)

    class Meta:
        table_name = 'person_has_role'
        indexes = (
            (('person', 'role'), True),
        )
        primary_key = CompositeKey('person', 'role')

class PersonWorkRelation(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'person_work_relation'

class Work(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'work'

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

class Script(BaseModel):
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'script'

class Subject(BaseModel):
    description = CharField(column_name='Description', null=True)
    name = CharField(column_name='Name')
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'subject'

class Tagsubject(BaseModel):
    belongsto = ForeignKeyField(column_name='BelongsTo', field='id', model='self', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'tagsubject'

class SubjectHasTag(BaseModel):
    subject = ForeignKeyField(column_name='subject', field='id', model=Subject)
    tag = ForeignKeyField(column_name='tag', field='id', model=Tagsubject)

    class Meta:
        table_name = 'subject_has_tag'
        indexes = (
            (('subject', 'tag'), True),
        )
        primary_key = CompositeKey('subject', 'tag')

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

class Tag(BaseModel):
    belongsto = ForeignKeyField(column_name='BelongsTo', field='id', model='self', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'tag'

class Tagwork(BaseModel):
    belongsto = ForeignKeyField(column_name='BelongsTo', field='id', model='self', null=True)
    name = CharField(column_name='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'tagwork'

class WorkHasTag(BaseModel):
    tag = ForeignKeyField(column_name='tag', field='id', model=Tagwork)
    work = ForeignKeyField(column_name='work', field='id', model=Work)

    class Meta:
        table_name = 'work_has_tag'
        indexes = (
            (('work', 'tag'), True),
        )
        primary_key = CompositeKey('tag', 'work')

class WorkInLanguage(BaseModel):
    language = ForeignKeyField(column_name='Language', field='id', model=Language)
    location = CharField(column_name='Location', null=True)
    work = ForeignKeyField(column_name='Work', field='id', model=Work)

    class Meta:
        table_name = 'work_in_language'
        indexes = (
            (('work', 'language'), True),
        )
        primary_key = CompositeKey('language', 'work')

class WorkInScript(BaseModel):
    location = CharField(column_name='Location', null=True)
    script = ForeignKeyField(column_name='Script', field='id', model=Script)
    work = ForeignKeyField(column_name='Work', field='id', model=Work)

    class Meta:
        table_name = 'work_in_script'
        indexes = (
            (('work', 'script'), True),
        )
        primary_key = CompositeKey('script', 'work')

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

