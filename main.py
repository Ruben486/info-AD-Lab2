import os
import platform
from productos_py_poo import (
    ProductoCelular,
    ProductoComputadora,
    GestionProductos
)
def clear_pantalla():
    '''Limpiar pantalla del SO'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') 
        
def menu_sistema():
    print(f"---------------------------------------------------------")
    print(f"---------------Menu de Sistema de Productos--------------")
    print(f"")
    print(f"1- Agregar Producto Teléfono Móvil")
    print(f"2- Alta producto computadora")
    print(f"3- Consulta datos de producto por Código")
    print(f"4- Actualizar precio de producto")
    print(f"5- Baja producto a través de Codigo")
    print(f"6- Mostrar todos los productos")
    print(f"7- Actualizar existencias de producto")
    print(f"8- Actualizar producto")
    print(f"9- Salir del sistema")
    print(f"")
    print(f"")
    print(f"---------------------------------------------------------")
    
def pausa_display():    
    input(f"Presione una tecla para continuar ->: ")

def ingresar_precio(precio_actual):
    try:
       precio = float(input(f"Ingrese precio del producto (Actual:  {precio_actual}): "))
       if precio >= 0:
          return precio
       print(f'El valor ingresado no corresponde a un precio')    
    except Exception as error:
       print(f'El valor ingresado no es un precio valido {error}')  
       
def ingresar_exixtencia(stk_actual):
    try:
       existencia = float(input(f"Ingrese existencias del producto (Actual {stk_actual}): "))  
       if existencia >= 0:
          return existencia
       else:
          print(f'El valor ingresado no es válido ')
          return None
    except Exception as error:
       print(f'El valor ingresado no es válido.Error: {error}')               
         
def ingreso_de_datos(codigo,opcion_producto,operacion,precio_ac,stock_ac):
    if operacion == "A":
       codigo = input("Código del producto: ")
       
    descripcion = input( "ingrese descripción: ")
    rubro = input("Ingrese Rubro del producto: ")   
    precio = ingresar_precio(precio_ac)
    existencias = ingresar_exixtencia(stock_ac)
    if precio and existencias:
       so = input("Ingrese SO del producto:")    
       if opcion_producto == '1':
          marca = input("Ingrese marca del producto: ")
          modelo = input("Ingrese modelo del producto: ")
          producto = ProductoCelular(codigo,descripcion,rubro,precio,existencias,so,marca,modelo)
        
       elif opcion_producto == '2':
          procesador = input("Ingrese Procesador del computador:")
          producto = ProductoComputadora(codigo,descripcion,rubro,precio,existencias,so,procesador)    
       return producto        

def agregar_producto(gestion,opcion_producto):
    try:
       producto = ingreso_de_datos('',opcion_producto,'A',0,0)        
       gestion.crear_producto(producto)
       print(f"Alta de producto ejecutada exitosamente")
        
    except ValueError as error:
       print(f"Ha sucedido un error: {error}")
    except Exception as error:
       print(f"Se produjo el siguiente error: {error}")    
    finally:
       pausa_display()
        
def actualizar_producto(gestion):        
    try:
        codigo = input(f"ingrese el código del producto a actualizar: ")
        producto = gestion.leer_producto(codigo)
        if producto:
            print(f'{producto}')
            if isinstance(producto,ProductoCelular):
                producto_actualizado = ingreso_de_datos(codigo,'1','M',producto.precio,producto.existencias)
            else:
                producto_actualizado = ingreso_de_datos(codigo,'2','M',producto.precio,producto.existencias)
            gestion.actualizar_producto(producto_actualizado)    
            
        else:
            print(f'No existe un producto con el código ingresado')
    except Exception as error:
        print(f"Se ha producido un error durante la actualizacion {error}")     
    pausa_display()
    
def buscar_producto_codigo(gestion):
    codigo = input(f"Ingrese código a buscar: ")
    producto = gestion.leer_producto(codigo)
    if producto:
        print(f'{producto}')
    else:
        print(f'No existe un producto con el código solicitado')    
    pausa_display()
    
        
def mostrar_productos(gestion):
    print(f"Listado General de Productos")
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    try:
        lista_productos = gestion.leer_todos_los_productos()
        for un_producto in lista_productos:
           item = lista_productos.index(un_producto) + 1
           print(f' {item}) {un_producto}')
           
    except Exception as error:
        print(f'Error {error} durante el listado general de productos')
    
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    pausa_display()
    
def actualizar_precio_producto(gestion):
    codigo = input(f"ingrese codigo de Producto: ")
    producto = gestion.leer_producto(codigo)
    if producto:
        try:
            precio = ingresar_precio(producto.precio)
            if precio:
                gestion.actualizar_precio_producto(codigo,precio)
        except Exception as error:
            print(f'El valor ingresado no es un precio valido')    
    else:
        print(f"El código ingresado no existe")  
    pausa_display()
    
def baja_producto(gestion):
    codigo = input(f"ingrese el codigo del producto a eliminar: ")
    gestion.eliminar_producto(codigo)
    pausa_display()
    
def actualizar_existencia_producto(gestion):
    codigo = input(f"ingrese el codigo del producto a actualizar: ")
    producto = gestion.leer_producto(codigo) 
    if producto:
       try:
          existencia = ingresar_exixtencia(producto.existencias)  
          if existencia:
            gestion.actualizar_stock_producto(codigo,existencia)
       except Exception as error:
           print(f'Se produjo un error durante la actualización {error}')     
    else:
       print(f"El codigo ingresado no existe")   
    pausa_display()
    
if __name__ == '__main__':
    gestion = GestionProductos()
    while True:
        clear_pantalla()
        menu_sistema()
        opcion = input("seleccione una opción->: ")
        if opcion == '1' or opcion == '2':
            agregar_producto(gestion,opcion) 
        elif opcion == '3':
            buscar_producto_codigo(gestion)  
        elif opcion == '4':
            actualizar_precio_producto(gestion)    
        elif opcion == '5':
            baja_producto(gestion)    
        elif opcion == '6':
            mostrar_productos(gestion)
        elif opcion == '7':
            actualizar_existencia_producto(gestion)   
        elif opcion == '8':
            actualizar_producto(gestion)     
        elif opcion == '9':
            print(f"Fin del programa")
            break
        else:
            print(f"Opción inexistente. Seleccione una opción válida")
            pausa_display()