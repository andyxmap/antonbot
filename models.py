from sqlalchemy import Column, Integer, String, Float, PickleType, Boolean, JSON, ForeignKey, LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship


Base = declarative_base()

# Disabling same thread checking for different users being able to watch all products
# engine = create_engine('sqlite:///db.sqlite?check_same_thread=False',echo=False)

engine = create_engine('postgresql://postgres:dariela1109@localhost:5433/antbot',echo=False,pool_pre_ping=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    carrito = relationship('Deseo')
    nombre = Column(String)
    alias = Column(String)
    baneado = Column(Boolean)
    admin = Column(Boolean)
    nombrecompleto = Column(String)
    carnet = Column(String)
    direccion = Column(String)
    numerotelefono = Column(String)


    def __repr__(self):
        return f'''```
Usuario -> {self.nombre}
Alias -> @{self.alias}
T_id -> {self.tg_id}
Ban -> {self.baneado}
Nombre Completo -> {self.nombrecompleto}
Carnet -> {self.carnet}
Direccion -> {self.direccion}
Numero Telefono -> {self.numerotelefono}

        ```'''

    @classmethod
    def limpiar_carrito(self):
        self.carrito = []

    def clone(self):
        return User(**self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'tg_id': self.tg_id,
            'carrito': self.carrito,
            'nombre': self.nombre,
            'alias': self.alias,
            'baneado': self.baneado,
            'nombrecompleto': self.nombrecompleto,
            'carnet': self.carnet,
            'control': self.control,
            'state': self.state,
        }




class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, unique=True ,primary_key=True)
    nombre = Column(String)
    detalles = Column(String)
    precio = Column(Float)
    categoria = Column(String)
    imagen = Column(String)
    limite = Column(Integer)
    deseado = relationship("Deseo",back_populates="producto",cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Producto: {self.nombre} , {self.detalles} , {self.precio}, {self.categoria}>'


class Deseo(Base):
    __tablename__ = 'deseo'

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    id_producto = Column(Integer,ForeignKey('producto.id'))
    producto = relationship("Producto",back_populates="deseado")
    cantidad = Column(Integer)

    def __repr__(self):
        return f'<Deseo: {self.id} , {self.user_id} , {self.cantidad}>'

class Utils(Base):
    __tablename__ = 'utils'

    id = Column(Integer,primary_key = True)
    categorias=Column(String)
    dev = Column(Integer)
    p_mostrados = Column(Integer)
    owner = Column(Integer)
    image_secs = Column(String)
    response_waiting = Column(Integer)

    def __repr__(self):
        return f'<Utils: {self.id} , {self.categorias} , {self.dev} , {self.p_mostrados} , {self.owner}>'


Session = scoped_session(sessionmaker(bind=engine))

session = Session()

session.close()
