from sqlalchemy_utils import create_database,database_exists,drop_database
from models import engine,Base
from models import User,Deseo,Producto,Utils
from repository import insert_user

def create_bot_database():
    if database_exists(engine.url):
        print('Database exists in')
    else:
        create_database(engine.url)
        print('Database are created {0}'.format(database_exists(engine.url)))

def delete_bot_database():
    drop_database(engine.url)

def populate():
    dev_info = {
        'tg_id': '1671749074',
        'carrito': [],
        'nombre': 'Andyx',
        'alias': ' ',
        'baneado': False,
        'admin': True,
        'nombrecompleto': 'Andy Hernandez Albulquerque',
        'direccion': 'La Habana',
        'numerotelefono': '58878991',
    }
    admin_info = {
        'tg_id': '628775092',
        'carrito': [],
        'nombre': 'Dayan',
        'alias': '@Anthond',
        'baneado': False,
        'admin': True,
        'nombrecompleto': 'Dayan Antonio Perez',
        'direccion': '',
        'numerotelefono': '55244400',
    }

    insert_user(dev_info)
    insert_user(admin_info)


if __name__ == '__main__':
    try:
     Base.metadata.create_all(engine)
     populate()
     print('Database create and populate')
    except Exception as e:
        print(e.__str__())