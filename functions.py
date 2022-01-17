from models import Producto, User, session, Base, engine, Deseo, Utils
from datetime import datetime
import calendar

def is_msg_too_old(message,bot,waiting):
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    difference = unixtime - message.date
    if difference > waiting:
        bot.send_message(message.from_user.id,"Este mensaje quedó obsoleto, reintente por favor.")
        return True
    return False

#know user use case
def check_user(id):
    user = session.query(User).filter_by(tg_id = id).first()
    return True if user else False

def init_utils():

    utils = session.query(Utils).filter_by(dev=1671749074).first()
    if utils:
       
        return utils
    else:

        utils = Utils(
            dev=1671749074,
            categorias='Alimentos 🥩 Aseo 🧼 Útiles del hogar 🏠 Otros 🎰',
            p_mostrados=3,
            owner=1671749074,
            image_secs='Nombre ✍️ Detalles 📋 Precio 💰 Limite 📦 Foto 🖼 Regresar ↩️',
            response_waiting=500
        )

        session.add(utils)

        session.commit()
        utils = session.query(Utils).filter_by(dev=1671749074).first()
        return utils

def get_user(msg):
    "Returns or creates a new user"
    user_id = msg.from_user.id
    user = session.query(User).filter_by(tg_id = user_id).first()

    if user:
        return user
    else:
        tg_id = msg.from_user.id 
        first_name = msg.from_user.first_name
        username = msg.from_user.username  
        if tg_id == 716072728 or 1671749074:
            user = User(
              tg_id = tg_id,
              nombre = first_name,
              alias = username,
              carrito= [],
              baneado = False,
              admin = True
        )
        else:
            user = User(
                tg_id = tg_id,
                nombre = first_name,
                alias = username,
                carrito= [],
                baneado = False,
                admin = False
            )
        session.add(user)
        session.commit()
        
        return user

def get_producto(msg):
    "Returns or creates a new product"
    nombre = msg.text
    producto = session.query(Producto).filter_by(nombre = nombre).first()

    if producto:
        return producto
    else:
        producto = Producto(nombre=nombre)
  
        return producto

def get_producto_por_id(p_id):
    producto = session.query(Producto).filter_by(id = p_id).first()
    if producto:
        return producto
    else:
        return "None"

def get_user_por_id(u_id):
    user = session.query(User).filter_by(tg_id = u_id).first()
    if user:
       return user
    else:
       return "El usuario no existe"


def get_usuarios_baneados():
    usuarios = session.query(User).filter_by(baneado = True).all()
    ids = []
    for usuario in usuarios:
        ids.append(usuario.tg_id)
    return ids

def get_admins():
    usuarios = session.query(User).filter_by(admin = True).all()
    ids = []
    for usuario in usuarios:
        ids.append(usuario.tg_id)
    return ids

def count_productos():
    length = session.query(Producto).count()
    return length

def create_db():
    try:
      Base.metadata.create_all(engine)
      print("Base de datos creada!")
    except Exception as e:
        print(e.__str__())

def del_db():
    session.query(User).delete()
    session.commit()
    print("Base de datos eliminada totalmente") 

#Obtiene el producto de mayor id
def get_recent_product():
    index = session.query(Producto).count()
    return session.query(Producto).get(index)

def get_usuarios():
    usuarios = session.query(User).all()
    if usuarios:
        return usuarios
    else:
        return []

def get_productos_por_categoria(cat):
    productos = session.query(Producto).filter_by(categoria=cat).all()
    if productos:
        return productos
    else:
        return []

def get_cantidad_en_categoria(cat):
    length = session.query(Producto).filter_by(categoria=cat).count()
    return length

def del_producto(producto):
    session.delete(producto)
    session.commit()

def get_deseo(producto,user):
    for deseo in user.carrito:
        if producto.id == deseo.producto.id:
            return deseo
   
    nuevo_deseo = Deseo(producto= producto, cantidad=0)
    user.carrito.append(nuevo_deseo)
    session.commit()

    return nuevo_deseo

def existe_deseo(producto,user):
    for deseo in user.carrito:
        if producto.id == deseo.producto.id:
            return deseo
    return None

def cantidad_de_producto_en_carro_t(producto,user):

    carrito = user.carrito

    # Si no esta vacio :
    if carrito:

        # Por cada par evalua hasta encontrar la cantidad
        for deseo in carrito:
                if deseo.id_producto == producto.id:
                    cantidad = deseo.cantidad
    # Si esta vacio, devuelve 0
    else:                 
        cantidad = 0
    
    return cantidad
