from peewee import *

database = MySQLDatabase('knowledgetree', **{'password': 'root123', 'port': 3306, 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Country(BaseModel):
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'country'

class State(BaseModel):
    country = ForeignKeyField(db_column='Country_id', rel_model=Country, to_field='id')
    name = CharField(db_column='Name', null=True)
    id = CharField()

    class Meta:
        db_table = 'state'
        indexes = (
            (('id', 'country'), True),
        )
        primary_key = CompositeKey('country', 'id')

class City(BaseModel):
    country = ForeignKeyField(db_column='Country_id', rel_model=State, to_field='country')
    name = CharField(db_column='Name', null=True)
    state = ForeignKeyField(db_column='State_id', rel_model=State, related_name='state_state_set', to_field='id')
    id = CharField()

    class Meta:
        db_table = 'city'
        indexes = (
            (('id', 'state', 'country'), True),
            (('state', 'country'), False),
        )
        primary_key = CompositeKey('country', 'id', 'state')

class District(BaseModel):
    country = ForeignKeyField(db_column='Country_id', rel_model=State, to_field='country')
    name = CharField(db_column='Name', null=True)
    state = ForeignKeyField(db_column='State_id', rel_model=State, related_name='state_state_set', to_field='id')
    id = CharField()

    class Meta:
        db_table = 'district'
        indexes = (
            (('id', 'state', 'country'), True),
            (('state', 'country'), False),
        )
        primary_key = CompositeKey('country', 'id', 'state')

class Person(BaseModel):
    biography = CharField(db_column='Biography', null=True)
    birth = DateField(db_column='Birth', null=True)
    death = DateField(db_column='Death', null=True)
    first = CharField(db_column='First', null=True)
    initials = CharField(db_column='Initials', null=True)
    last = CharField(db_column='Last', null=True)
    living = IntegerField(db_column='Living', null=True)
    middle = CharField(db_column='Middle', null=True)
    nick = CharField(db_column='Nick', null=True)
    other = CharField(db_column='Other', null=True)
    period = CharField(db_column='Period', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'person'

class Address(BaseModel):
    area = CharField(db_column='Area', null=True)
    city_country = ForeignKeyField(db_column='City_Country_id', null=True, rel_model=City, to_field='country')
    city_state = ForeignKeyField(db_column='City_State_id', null=True, rel_model=City, related_name='city_city_state_set', to_field='state')
    city = ForeignKeyField(db_column='City_id', null=True, rel_model=City, related_name='city_city_set', to_field='id')
    district_country = ForeignKeyField(db_column='District_Country_id', null=True, rel_model=District, to_field='country')
    district_state = ForeignKeyField(db_column='District_State_id', null=True, rel_model=District, related_name='district_district_state_set', to_field='state')
    district = ForeignKeyField(db_column='District_id', null=True, rel_model=District, related_name='district_district_set', to_field='id')
    housenumber = CharField(db_column='HouseNumber', null=True)
    person = ForeignKeyField(db_column='Person', null=True, rel_model=Person, to_field='id')
    street = CharField(db_column='Street', null=True)
    value = CharField(db_column='Value', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'address'
        indexes = (
            (('city', 'city_state', 'city_country'), False),
            (('district', 'district_state', 'district_country'), False),
        )

class Affiliation(BaseModel):
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'affiliation'

class Language(BaseModel):
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'language'

class PersonHasAffiliation(BaseModel):
    affiliation = ForeignKeyField(db_column='affiliation', rel_model=Affiliation, to_field='id')
    person = ForeignKeyField(db_column='person', rel_model=Person, to_field='id')

    class Meta:
        db_table = 'person_has_affiliation'
        indexes = (
            (('person', 'affiliation'), True),
        )
        primary_key = CompositeKey('affiliation', 'person')

class Role(BaseModel):
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'role'

class PersonHasRole(BaseModel):
    person = ForeignKeyField(db_column='person', rel_model=Person, to_field='id')
    role = ForeignKeyField(db_column='role', rel_model=Role, to_field='id')

    class Meta:
        db_table = 'person_has_role'
        indexes = (
            (('person', 'role'), True),
        )
        primary_key = CompositeKey('person', 'role')

class Work(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'work'

class PersonWorkRelation(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'person_work_relation'

class PersonHasWork(BaseModel):
    person = ForeignKeyField(db_column='Person', rel_model=Person, to_field='id')
    relation = ForeignKeyField(db_column='Relation', rel_model=PersonWorkRelation, to_field='id')
    work = ForeignKeyField(db_column='Work', rel_model=Work, to_field='id')

    class Meta:
        db_table = 'person_has_work'
        indexes = (
            (('person', 'work', 'relation'), True),
        )
        primary_key = CompositeKey('person', 'relation', 'work')

class PersonPersonRelation(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'person_person_relation'

class PersonRelatestoPerson(BaseModel):
    person1 = ForeignKeyField(db_column='person1', rel_model=Person, to_field='id')
    person2 = ForeignKeyField(db_column='person2', rel_model=Person, related_name='person_person2_set', to_field='id')
    relation = ForeignKeyField(db_column='relation', rel_model=PersonPersonRelation, to_field='id')

    class Meta:
        db_table = 'person_relatesto_person'
        indexes = (
            (('person1', 'person2', 'relation'), True),
        )
        primary_key = CompositeKey('person1', 'person2', 'relation')

class Script(BaseModel):
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'script'

class Subject(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name')
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'subject'

class Tagsubject(BaseModel):
    belongsto = ForeignKeyField(db_column='BelongsTo', null=True, rel_model='self', to_field='id')
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'tagsubject'

class SubjectHasTag(BaseModel):
    subject = ForeignKeyField(db_column='subject', rel_model=Subject, to_field='id')
    tag = ForeignKeyField(db_column='tag', rel_model=Tagsubject, to_field='id')

    class Meta:
        db_table = 'subject_has_tag'
        indexes = (
            (('subject', 'tag'), True),
        )
        primary_key = CompositeKey('subject', 'tag')

class WorkSubjectRelation(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'work_subject_relation'

class SubjectHasWork(BaseModel):
    relation = ForeignKeyField(db_column='Relation', rel_model=WorkSubjectRelation, to_field='id')
    subject = ForeignKeyField(db_column='Subject', rel_model=Subject, to_field='id')
    work = ForeignKeyField(db_column='Work', rel_model=Work, to_field='id')

    class Meta:
        db_table = 'subject_has_work'
        indexes = (
            (('subject', 'work', 'relation'), True),
        )
        primary_key = CompositeKey('relation', 'subject', 'work')

class SubjectSubjectRelation(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'subject_subject_relation'

class SubjectRelatestoSubject(BaseModel):
    relation = ForeignKeyField(db_column='Relation', null=True, rel_model=SubjectSubjectRelation, to_field='id')
    sortorder = IntegerField(db_column='Sortorder', null=True)
    subject1 = ForeignKeyField(db_column='Subject1', rel_model=Subject, to_field='id')
    subject2 = ForeignKeyField(db_column='Subject2', rel_model=Subject, related_name='subject_subject2_set', to_field='id')

    class Meta:
        db_table = 'subject_relatesto_subject'
        indexes = (
            (('subject1', 'subject2'), True),
        )
        primary_key = CompositeKey('subject1', 'subject2')

class Tag(BaseModel):
    belongsto = ForeignKeyField(db_column='BelongsTo', null=True, rel_model='self', to_field='id')
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'tag'

class Tagwork(BaseModel):
    belongsto = ForeignKeyField(db_column='BelongsTo', null=True, rel_model='self', to_field='id')
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'tagwork'

class WorkHasTag(BaseModel):
    tag = ForeignKeyField(db_column='tag', rel_model=Tagwork, to_field='id')
    work = ForeignKeyField(db_column='work', rel_model=Work, to_field='id')

    class Meta:
        db_table = 'work_has_tag'
        indexes = (
            (('work', 'tag'), True),
        )
        primary_key = CompositeKey('tag', 'work')

class WorkInLanguage(BaseModel):
    language = ForeignKeyField(db_column='Language', rel_model=Language, to_field='id')
    location = CharField(db_column='Location', null=True)
    work = ForeignKeyField(db_column='Work', rel_model=Work, to_field='id')

    class Meta:
        db_table = 'work_in_language'
        indexes = (
            (('work', 'language'), True),
        )
        primary_key = CompositeKey('language', 'work')

class WorkInScript(BaseModel):
    location = CharField(db_column='Location', null=True)
    script = ForeignKeyField(db_column='Script', rel_model=Script, to_field='id')
    work = ForeignKeyField(db_column='Work', rel_model=Work, to_field='id')

    class Meta:
        db_table = 'work_in_script'
        indexes = (
            (('work', 'script'), True),
        )
        primary_key = CompositeKey('script', 'work')

class WorkWorkRelation(BaseModel):
    description = CharField(db_column='Description', null=True)
    name = CharField(db_column='Name', null=True)
    id = CharField(primary_key=True)

    class Meta:
        db_table = 'work_work_relation'

class WorkRelatestoWork(BaseModel):
    relation = ForeignKeyField(db_column='Relation', null=True, rel_model=WorkWorkRelation, to_field='id')
    sortorder = IntegerField(db_column='Sortorder', null=True)
    work1 = ForeignKeyField(db_column='Work1', rel_model=Work, to_field='id')
    work2 = ForeignKeyField(db_column='Work2', rel_model=Work, related_name='work_work2_set', to_field='id')

    class Meta:
        db_table = 'work_relatesto_work'
        indexes = (
            (('work1', 'work2'), True),
        )
        primary_key = CompositeKey('work1', 'work2')

