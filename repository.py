from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User

#global engine for export session object
engine = create_engine('postgresql://postgres:dariela1109@localhost:5433/antbot',echo=False,pool_pre_ping=True)

def use_session():
    return sessionmaker(bind=engine)

def session_object():
    Session = use_session()
    session = Session()
    return  session

#use this line of code if you whant create a Db. Is some important import all models for do that
#Base.metadata.create_all(engine)

###### Functions plubics to access repository #####

## user model functions

def check_user(id):
    user = None
    with use_session()() as session:
        user = session.query(User).filter_by(tg_id = id).first()
        return True if user else False


def get_user_by_tg_id(id):
    "Returns or creates a new user"
    session = use_session()()
    user = session.query(User).filter_by(tg_id=id).first()

    return user,session

def get_all_user():

    session = use_session()()
    users = session.query(User).all()

    return users,session

def get_usuarios_baneados():
     users = []
     session = use_session()()
     users = session.query(User).filter_by(baneado = True).all()

     return users,session

def getadmins():

    session = use_session()()
    admins = session.query(User).filter_by(admin = True).all()
    admins = [admin.tg_id for admin in admins]

    session.close()
    return admins

def insert_user(user):
    new_user = User()
    with use_session()() as session:

        if isinstance(user,dict):
             new_user = User(**user)
        elif isinstance(user,User):
            new_user = user

        session.add(new_user)
        session.commit()

def update_user(user):
    with use_session()() as session:
        if isinstance(user,dict):
             user_update = session.query(User).filter(User.tg_id == user['tg_id']).first()
             for key,value in user.items():
                 setattr(user_update,key,value)
             session.commit()






####################################################



