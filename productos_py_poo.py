
""" 
Objetivo:
Sistema de Gestion de Productos

'''29.25 del 13/08'''
"""
import mysql.connector
from mysql.connector import Error
from decouple import config 


class Producto:
    def __init__(self, codigo, descripcion, rubro, precio, existencias):
        self.__codigo = codigo
        self.__descripcion = descripcion
        self.__rubro = rubro
        self.__precio = self.validar_precio(precio)
        self.__existencias = self.validar_existencias(existencias)

    @property
    def codigo(self):
        return self.__codigo 
    
    @property     
    def descripcion(self):
        return self.__descripcion
    
    @property
    def rubro(self):
        return self.__rubro
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def existencias(self):
        return self.__existencias
    
    @precio.setter
    def precio(self,nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    @existencias.setter
    def existencias(self,nuevas_existencias):
        self.__existencias = self.validar_existencias(nuevas_existencias)    
    
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "rubro": self.rubro,
            "precio": self.precio,
            "existencias": self.existencias
        }
        
    def __str__(self):
        return f"{self.__codigo} | {self.__descripcion} | Rubro: {self.rubro} | Precio: {self.precio} | Existencias: {self.existencias}"
    
    def validar_precio(self,precio):
        try:
            precio = float(precio) 
            if precio < 0:
                raise ValueError("Precio debe ser no negativo")
            return precio
        except:
            raise ValueError("Precio no es una variable numérica")
            return None
        
    def validar_existencias(self,existencias):
        try:
            stock = float(existencias)
            if stock < 0:
                raise ValueError("Las existencias deben ser no negativas")
            return stock
        except ValueError:
            raise ValueError("Existencias debe ser un valor numérico")
        
        
class ProductoCelular(Producto):
    def __init__(self, codigo, descripcion, rubro, precio, existencias, so, marca, modelo):
        super().__init__(codigo, descripcion, rubro, precio,existencias)
        self.__so = so
        self.__marca = marca
        self.__modelo = modelo

    @property
    def so(self):
        return self.__so
    
    @property
    def marca(self):
        return self.__marca
    
    @property
    def modelo(self):
        return self.__modelo
    
    def to_dict(self):
        """ return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "rubro": self.rubro,
            "precio": self.precio,
            "existencias": self.existencias,
            "sistema_operativo": self.so,
            "marca": self.marca,
            "modelo": self.modelo,
        } """
        data = super().to_dict()
        data["sistema_operativo"] = self.so
        data["marca"] = self.marca
        data["modelo"] = self.modelo
        return data 
        
    def __str__(self):
        return f"{super().__str__()} | Sistema Operativo: {self.__so} | Marca: {self.__marca}  | Modelo: {self.__modelo}"
    
class ProductoComputadora(Producto):
    def __init__(self, codigo, descripcion, rubro, precio, existencias, so, procesador):
        super().__init__(codigo, descripcion, rubro, precio,existencias)
        self.__so = so
        self.__procesador = procesador

    @property
    def so(self):
        return self.__so
    
    @property
    def procesador(self):
        return self.__procesador
    
    def to_dict(self):
        """ return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "rubro": self.rubro,
            "precio": self.precio,
            "existencias": self.existencias,
            "sistema_operativo": self.so,
            "marca": self.marca,
            "modelo": self.modelo,
        } """
        data = super().to_dict()
        data["sistema_operativo"] = self.so
        data["procesador"] = self.procesador
        return data 
        
    def __str__(self):
        return f"{super().__str__()} | Sistema Operativo: {self.__so} | Procesador: {self.__procesador}"
        
class GestionProductos:
    def __init__(self):
       self.host = config('DB_HOST')
       self.database = config('DB_NAME')
       self.user = config('DB_USER')
       self.password = config('DB_PASSWORD')
       self.port =  config('DB_PORT')
    
    def connect(self):
        '''Conexion a la base de datos MySQL'''
        ''' hay muchos controles que hacer con los parámetros'''
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password,
                port = self.port
            )        
            if connection.is_connected():
                return connection
              
        except Error as e:  
            print(f'Se ha producido un error al intentar conectar con la base de datos {e}')
            return None
            
    def cerrar_conexion(self,connection):
        if connection.is_connected():
            connection.close() 
    
    def altaProductoBase(self,cursor,producto):
        try:
            query = ''' INSERT INTO productos (Codigo,Descripcion,Rubro,Precio, Existencias, SO )
            VALUES (%s,%s,%s,%s,%s,%s)
            '''
            cursor.execute(query,(producto.codigo,producto.descripcion,producto.rubro,producto.precio,producto.existencias,producto.so)) 
            return True
        except Exception as Error:
            print(f"s produjo un error: {Error} al intentar dar de alta el producto Base con código {producto.codigo}")
            return False
        
    def destructurar_producto(self,tipo_producto,producto_data):
        '''
        tipo_producto: B:Base, C:Celular,P:Computadora
        '''    
        if tipo_producto == 'B':
            p_codigo,p_descripcion,p_rubro,p_precio,p_existencias,p_so = producto_data.values()
            producto = Producto(p_codigo,p_descripcion,p_rubro,p_precio,p_existencias,p_so)
            return producto
        elif tipo_producto == 'C':    
            p_codigo,p_descripcion,p_rubro,p_precio,p_existencias,p_so,p_marca,p_modelo = producto_data.values()
            producto = ProductoCelular(p_codigo,p_descripcion,p_rubro,p_precio,p_existencias,p_so,p_marca,p_modelo)
            return producto
        elif tipo_producto == 'P': 
            p_codigo,p_descripcion,p_rubro,p_precio,p_existencias,p_so,p_procesador = producto_data.values()
            producto = ProductoComputadora(p_codigo,p_descripcion,p_rubro,p_precio,p_existencias,p_so,p_procesador)
            return producto
        else:
            return 
        
    def crear_producto(self,producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT Codigo FROM productos WHERE Codigo = %s',(producto.codigo,))
                    if cursor.fetchone():
                        print(f"Error: Ya existe un producto con el código ingresado {producto.codigo}")
                        return
                    if isinstance(producto,ProductoCelular):
                        altaProductoBase = self.altaProductoBase(cursor,producto)
                        query = ''' 
                        INSERT INTO productoCelular (Codigo,Marca,Modelo)
                        VALUES (%s,%s,%s)
                        '''
                        cursor.execute(query,(producto.codigo, producto.marca, producto.modelo))
                    elif isinstance(producto,ProductoComputadora):
                        """     query = ''' INSERT INTO productos (Codigo,Descripcion,Rubro,Precio, Existencias, SO )
                        VALUES (%s,%s,%s,%s,%s,%s)
                        '''
                        cursor.execute(query,(producto.codigo,producto.descripcion,producto.rubro,producto.precio,producto.existencias,producto.so)) """ 
                        altaProductoBase = self.altaProductoBase(cursor,producto)
                        if altaProductoBase:
                           query = ''' 
                           INSERT INTO productoComputadora (Codigo,Procesador)
                           VALUES (%s,%s)
                           '''
                        cursor.execute(query,(producto.codigo, producto.procesador))
                    connection.commit()
                    print(f'Producto {producto.codigo} {producto.descripcion} creado exitosamente')        
        except Exception as error:
            print(f"Se produjo el error {error} al intentar crear el producto")
        finally:
            self.cerrar_conexion(connection)
                        
    def leer_producto(self,codigo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM productos WHERE Codigo = %s',(codigo,))
                    producto_data = cursor.fetchone() 
                    if producto_data:
                        cursor.execute('SELECT procesador FROM productocomputadora WHERE Codigo = %s',(codigo,))
                        procesador = cursor.fetchone()
                        if procesador:
                            producto_data['Procesador'] = procesador['procesador']
                            producto = self.destructurar_producto('P',producto_data)         
                        else:
                            cursor.execute('SELECT * FROM productoCelular WHERE codigo = %s',(codigo,))
                            marca = cursor.fetchone()                  
                            if marca:
                                producto_data['Marca']  = marca['Marca']
                                producto_data['Modelo'] = marca['Modelo']
                                producto = self.destructurar_producto('C',producto_data)
                            else:
                                producto = self.destructurar_producto('B',producto_data)
                        
                    else:
                        producto = None    
        except Error as e:
            print(f"Error al leer datos {e} producto: {codigo}")
        else:
            return producto    
        finally:
            self.cerrar_conexion(connection)
            
    def actualizar_producto(self,producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                   if producto:
                      query = '''
                      UPDATE productos SET Descripcion = %s,Rubro = %s,Precio = %s,Existencias = %s,SO = %s WHERE Codigo = %s 
                      '''
                      cursor.execute(query,(producto.descripcion,producto.rubro,producto.precio,producto.existencias,producto.so,producto.codigo))                 
                      
                      # Segunda parte de la actualizacion por el tipo producto  #
                      if isinstance(producto,ProductoCelular):
                         query = ''' 
                         UPDATE productoCelular SET Marca = %s, Modelo = %s
                         WHERE Codigo = %s
                         '''
                         cursor.execute(query,(producto.marca,producto.modelo,producto.codigo))   
                      elif isinstance(producto,ProductoComputadora):   
                         query = ''' 
                         UPDATE productoComputadora SET Procesador = %s WHERE Codigo = %s
                         '''
                         cursor.execute(query,(producto.procesador,producto.codigo))
                         
                      if cursor.rowcount > 0:
                         connection.commit()
                         print(f'Producto actualizado exitosamente')
                         
        except Exception as error:
            print(f'Se produjo un error durante la actualización del producto {error}')                
        finally:
            self.cerrar_conexion(connection)
                
    def actualizar_precio_producto(self,codigo,n_precio):
        try:
            connection = self.connect() 
            if connection:   
                with connection.cursor() as cursor:
                    producto = self.leer_producto(codigo)
                    if producto:
                        query = '''UPDATE productos SET Precio = %s WHERE Codigo = %s'''
                        cursor.execute(query,(n_precio,codigo))
                        if cursor.rowcount > 0:
                            connection.commit()
                            print(f'Se actualizó el registro exitosamente')
                        else:    
                            print(f'No se encontró el producto con codigo {codigo}')
                    else:
                        print(f'No existe un producto con el codigo ingresado')
            else:
                print(f'No se puedo realizar la conexion a la Base de Datos')
        except Error as error:
            print(f"Error {error} al intentar actualizar precio del producto con codigo {codigo}")                            
        finally:
            self.cerrar_conexion(connection)
            
    def actualizar_stock_producto(self,codigo,existencia):
        try:
           connection = self.connect() 
           if connection:   
              with connection.cursor() as cursor:
                 producto = self.leer_producto(codigo)
                 if producto:
                    query = '''UPDATE productos SET Existencias = %s WHERE Codigo = %s'''
                    cursor.execute(query,(existencia,codigo))
                    if cursor.rowcount > 0:
                       connection.commit()
                       print(f'Se actualizó el producto exitosamente')
                    else:    
                       print(f'No se encontró el producto con codigo {codigo}') 
        except Exception as error:
            print(f"Error al intentar actualizar existencias del producto con codigo {codigo}")     
                                           
    def eliminar_producto(self,codigo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:     
                    producto = self.leer_producto(codigo)
                    if not producto:
                        print(f'No existe un producto con el código solicitado {codigo}')
                        return None
                    # eliminacion del producto encontrado
                    cursor.execute('DELETE FROM productoCelular WHERE codigo = %s',(codigo,))
                    cursor.execute('DELETE FROM productoComputadora WHERE codigo = %s',(codigo,))
                    cursor.execute('DELETE FROM productos WHERE codigo = %s',(codigo,))    
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'El producto ha sido eliminado sin inconvenientes')
                    else:
                        print(f'No se encontro el producto con codigo {codigo} durante el proceso de eliminación')    
        except Error as error:
            print(f"Error {error} al intentar acceder a datos de {codigo}")
        finally:
            self.cerrar_conexion(connection)    
            
    def leer_todos_los_productos(self):
       try:
          connection = self.connect()
          if connection:
              with connection.cursor(dictionary=True) as cursor:     
                 cursor.execute('SELECT * FROM productos')
                 productos = cursor.fetchall()
                 lista_productos = []
                 for producto in productos:
                     codigo = producto['Codigo']
                     producto_leido = self.leer_producto(codigo)
                     if producto_leido:
                         lista_productos.append(producto_leido)                
                         
           
       except Error as error:
            print(f"Error {error} al intentar acceder a datos de todos los productos")
       else:
            return lista_productos       
       finally:
            self.cerrar_conexion(connection)    
         