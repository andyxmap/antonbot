from telebot import types
from functions import *
from models import User
import numpy as np
# ☑️ ✅ 🛒 ➡️ ⬅️ ↩️ 💰 Editar *️⃣  Eliminar ❌

#new botonera
def botonera_accept():
      keyboard = []
      yes = types.InlineKeyboardButton(
            text=f'Aceptar Terminos 👍',
            callback_data=f'yes'
      )
      no = types.InlineKeyboardButton(
            text=f'No Acepto los terminos 👎',
            callback_data=f'no'
      )
      keyboard.append([yes,no])
      markup = types.InlineKeyboardMarkup(keyboard)
      markup.row_width = 2
      return markup

def get_botonera_inicial():
      markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
      alimentosButton = types.KeyboardButton('Alimentos 🥩')
      aseoButton = types.KeyboardButton('Aseo 🧼')
      utilesButton = types.KeyboardButton('Útiles del hogar 🏠')
      otrosButton = types.KeyboardButton('Otros 🎰')
      markup.add(alimentosButton, aseoButton , utilesButton, otrosButton)
      return markup
      
def get_botonera_admin():
      markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
      alimentosButton = types.KeyboardButton('Alimentos 🥩')
      aseoButton = types.KeyboardButton('Aseo 🧼')
      utilesButton = types.KeyboardButton('Útiles del hogar 🏠')
      otrosButton = types.KeyboardButton('Otros 🎰')
      agregarButton = types.KeyboardButton("Agregar Producto ➕")
      markup.add(alimentosButton, aseoButton , utilesButton, otrosButton,agregarButton)
      return markup

def get_botonera_agregando_producto():
      markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
      returnButton = types.KeyboardButton("Cancelar ↩️")
      markup.add(returnButton)
      return markup

def get_botonera_edicion_producto():

      markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)

      nombreButton = types.KeyboardButton("Nombre ✍️") 
      detallesButton = types.KeyboardButton ("Detalles 📋")
      precioButton = types.KeyboardButton("Precio 💰")
      limiteButton = types.KeyboardButton("Limite 📦")
      fotoButton = types.KeyboardButton("Foto 🖼")
      returnButton = types.KeyboardButton("Regresar ↩️")

      markup.row(nombreButton,detallesButton)
      markup.row(precioButton,limiteButton)
      markup.row(fotoButton,returnButton)
      return markup
      
def get_productos_menu():
      comprarButton = types.KeyboardButton('Hacer compra 💰')
      carritoButton = types.KeyboardButton('Carrito 🛒')
      deshacerButton = types.KeyboardButton('Regresar ↩️')
      
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.row(comprarButton)
      markup.row(carritoButton,deshacerButton)

      return markup

def get_botonera_carrito():
      
      comprarButton = types.KeyboardButton('Hacer compra 💰')
      refrescarCarritoButton = types.KeyboardButton('Refrescar Carrito 🛒')
      vaciarCarritoButton = types.KeyboardButton('Vaciar carrito ♻️') 
      regresarButton = types.KeyboardButton('Regresar ↩️')
      
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.row(comprarButton,refrescarCarritoButton)
      markup.row(vaciarCarritoButton,regresarButton)

      return markup

def info_renovar_botonera():
      sms = '''```
   ⚠️Advertencia⚠️
El producto sobre el cual desea
consultar, ha sido renovado o eliminado
. Porfavor vuelva a consultar los productos
directamente desde las categorías.
      ```'''
      return sms

def info_producto_para_carrito(nombre,precio,cantidad):
      sms = f'''```
\n{cantidad}x {nombre} ({precio} mlc)```'''
      return sms

def get_botonera_cancelar(categorias):
      markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
      if categorias:
            alimentosButton = types.KeyboardButton('Alimentos 🥩')
            aseoButton = types.KeyboardButton('Aseo 🧼')
            utilesButton = types.KeyboardButton('Útiles del hogar 🏠')
            otrosButton = types.KeyboardButton('Otros 🎰')
            cancelarButton = types.KeyboardButton('Cancelar ↩️')
            markup.add(alimentosButton, aseoButton , utilesButton,otrosButton,cancelarButton)
      else:
            cancelarButton = types.KeyboardButton('Cancelar ↩️')
            markup.add(cancelarButton)
      return markup

def get_inline_b(producto,user,len,cantidad,index,admin):

      keyboard = []

      # Buscamos la cantidad temporal, no real:
      # cantidad = cantidad_de_producto_en_carro_t(producto,user)

      # ide del producto
      p_id = producto.id

      categoria = producto.categoria

      length = get_cantidad_en_categoria(categoria) - 1

      print(f'Showing index :{index} , length: {length}')

      if cantidad > 0 :
            emoji_check = "✅"
      else:
            emoji_check = "☑️"

      emoji_carrito = "🛒"
      emoji_sgt = "➡️"
      emoji_ant = "⬅️"

      # agregando botonera
      comprarButton = types.InlineKeyboardButton(
                              text= f'Cantidad a comprar: {cantidad} {emoji_check}',
                              callback_data= f'charge_{p_id}_{cantidad}_{index}_{categoria}'
                        )

      descontar_carritoButton = types.InlineKeyboardButton(
                              text = f'Bajar una unidad {emoji_carrito}',
                              callback_data= f'reduce_{p_id}_{cantidad}_{index}_{categoria}'
                        )

      keyboard.append([comprarButton])
      keyboard.append([descontar_carritoButton])

      sgte = False
      ant = False

      if index < length:   
            sgte = True
      
      if index > 0 or (index == length and length!=0):
            ant = True
           
      arrows = []

      if ant :

            antButton = types.InlineKeyboardButton(
                        text = f'{emoji_ant}',
                        callback_data=f'prev_{index}_{categoria}'
                  )
            
            arrows.append(antButton)

      if sgte:

            sgteButton = types.InlineKeyboardButton(
                        text = f'{emoji_sgt}',
                        callback_data=f'next_{index}_{categoria}'
                  )
            
            arrows.append(sgteButton)
      
      if arrows != []:
            keyboard.append(arrows)      
  
      if admin:

            editarButton = types.InlineKeyboardButton(
                        text = f'Editar *️⃣',
                        callback_data=f'edit_{p_id}'
                  )
            
            eliminarButton = types.InlineKeyboardButton(
                  text = f'Eliminar ❌',
                  callback_data=f'delete_{p_id}'
            )

            keyboard.append([editarButton,eliminarButton])

      markup = types.InlineKeyboardMarkup(keyboard)
      markup.row_width = 2
      
      return markup 

def welcome_message():
      return '''```
      Términos y condiciones 

TraiGo! Es una tienda online con el único objetivo facilitar la experiencia de compra de nuestros clientes y a la vez está sea gratificante.

Por tanto, No vendemos a sobre precio y para evitar el acaparamiento en nuestra tienda cada cliente dispone de una capacidad de compra razonable que le permita satisfacer sus necesidades sin que esta afecte a terceros. Dicha capacidad de compra irá aumentando según nuestra disponibilidad de productos.

Pronto iremos agregando más opciones a nuestro servicio para que usted quede aún más complacido/a

Para más información y estar al tanto de nuestras ofertas síganos en nuestro canal https://t.me/TraiGoCanal

Si tiene alguna duda o sugerencia contáctenos a través del siguiente usuario @Anthond

Saludos
    ```'''

def comandos_info():
      sms = '''
      ```
/decir <id> - <texto>  -> Envia el texto al usuario segun su id

/ban <id> -> Banea al usuario

/unban <id> -> Desbanea al usuario

/i_u <id> -> Inspecciona al usuario

/anunciar <texto> -> Envia el texto a todos los usuarios
      ```
      '''

      return sms

def hacer_sms_producto(producto):
      sms = f'''```
{producto.nombre}

{producto.detalles}

Precio: {producto.precio} mlc

Puede comprar {producto.limite} unidades 
                        ```'''
      return sms