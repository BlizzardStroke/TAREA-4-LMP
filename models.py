from peewee import *

database = MySQLDatabase('world',
                         **{'charset': 'utf8',
                            'sql_mode': 'PIPES_AS_CONCAT',
                            'use_unicode': True,
                            'host': 'localhost',
                            'user': 'root',
                            'password': '1234'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Country(BaseModel):
    capital = IntegerField(column_name='Capital', null=True)
    code = CharField(column_name='Code', constraints=[SQL("DEFAULT ''")], primary_key=True)
    code2 = CharField(column_name='Code2', constraints=[SQL("DEFAULT ''")])
    continent = CharField(column_name='Continent', constraints=[SQL("DEFAULT 'Asia'")])
    gnp = FloatField(column_name='GNP', null=True)
    gnp_old = FloatField(column_name='GNPOld', null=True)
    government_form = CharField(column_name='GovernmentForm', constraints=[SQL("DEFAULT ''")])
    head_of_state = CharField(column_name='HeadOfState', null=True)
    indep_year = IntegerField(column_name='IndepYear', null=True)
    life_expectancy = FloatField(column_name='LifeExpectancy', null=True)
    local_name = CharField(column_name='LocalName', constraints=[SQL("DEFAULT ''")])
    name = CharField(column_name='Name', constraints=[SQL("DEFAULT ''")])
    population = IntegerField(column_name='Population', constraints=[SQL("DEFAULT 0")])
    region = CharField(column_name='Region', constraints=[SQL("DEFAULT ''")])
    surface_area = FloatField(column_name='SurfaceArea', constraints=[SQL("DEFAULT 0.00")])

    class Meta:
        table_name = 'country'


class City(BaseModel):
    country_code = ForeignKeyField(column_name='CountryCode', constraints=[SQL("DEFAULT ''")], field='code', model=Country)
    district = CharField(column_name='District', constraints=[SQL("DEFAULT ''")])
    id = AutoField(column_name='ID')
    name = CharField(column_name='Name', constraints=[SQL("DEFAULT ''")])
    population = IntegerField(column_name='Population', constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'city'


class Countrylanguage(BaseModel):
    country_code = ForeignKeyField(column_name='CountryCode', constraints=[SQL("DEFAULT ''")], field='code', model=Country)
    is_official = CharField(column_name='IsOfficial', constraints=[SQL("DEFAULT 'F'")])
    language = CharField(column_name='Language', constraints=[SQL("DEFAULT ''")])
    percentage = FloatField(column_name='Percentage', constraints=[SQL("DEFAULT 0.0")])

    class Meta:
        table_name = 'countrylanguage'
        indexes = (
            (('country_code', 'language'), True),
        )
        primary_key = CompositeKey('country_code', 'language')


Monterrey = City( country_code='ABW',
                  district='Nuevo Leon',
                  id=20001,
                  name='Monterrey',
                  population=5120000)
Monterrey.save()


query = (City
        .select(City.country_code, City.name, City.population)
        .where(City.country_code == 'BRA'))

print('\nPrimer query WHERE')
for ciudad in query:
   print('Country Code: {} Name: {} Population: {} '
   .format(ciudad.country_code,
           ciudad.name,
           ciudad.population))

query = (City
        .select(City.country_code, City.name, City.population)
        .order_by(City.population))

print('\nSegundo query Order By')
for ciudad in query:
   print('Country Code: {} Name: {} Population: {} '
   .format(ciudad.country_code,
           ciudad.name,
           ciudad.population))

print('\nTercer query Insert')
query = (City
        .select(City.country_code, City.name, City.population)
        .where(City.id == 20001))

for ciudad in query:
   print('Country Code: {} Name: {} Population: {} '
   .format(ciudad.country_code,
           ciudad.name,
           ciudad.population))

