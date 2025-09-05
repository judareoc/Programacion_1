from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# -------------------- Clase Producto --------------------
class Producto:
    def __init__(self, nombre:str, precio:float, cantidad:int):
        self.__nombre = nombre       # privado
        self.__precio = precio       # privado
        self.__cantidad = cantidad   # privado

    def get_nombre(self)->str:
        return self.__nombre

    def get_precio(self)->float:
        return self.__precio

    def get_cantidad(self)->int:
        return self.__cantidad

    def set_cantidad(self, cantidad:int)->None:
        if cantidad >= 0:
            self.__cantidad = cantidad
            
    def verificar_disponibilidad(self, cantidad:int)->bool:
        return self.__cantidad >= cantidad

    def actualizar_stock(self, cantidad:int)->bool:
        if self.verificar_disponibilidad(cantidad):
            self.__cantidad -= cantidad
            return True
        return False

    def subtotal(self, cantidad:int)->float:
        return self.__precio * cantidad
    
    
class Caja:
    def __init__(self):
        self.ingresos = 0
        self.egresos = 0

    def registrar_ingreso(self, monto:float)->None:
        self.ingresos += monto

    def registrar_egreso(self, monto:float)->None:
        self.egresos += monto

    def balance(self)->float:
        return self.ingresos - self.egresos
    

# -------------------- Clase Cliente --------------------
class Cliente:
    def __init__(self, nombre:str, identificacion:str):
        self.__nombre = nombre
        self.__identificacion = identificacion

    def get_nombre(self)->str:
        return self.__nombre

    def get_identificacion(self)->str:
        return self.__identificacion


# -------------------- Clase Inventario --------------------
class Inventario:
    def __init__(self):
        self.__productos = []

    def agregar_producto(self, producto:str)->None:
        self.__productos.append(producto)

    def buscar_producto(self, nombre:str)->None:
        for producto in self.__productos:
            if producto.get_nombre().lower() == nombre.lower():
                return producto
        return None

    def mostrar_inventario(self)->None:
        print("\nInventario disponible:")
        for p in self.__productos:
            print(f"- {p.get_nombre()} | ${p.get_precio()} | Stock: {p.get_cantidad()}")


# -------------------- Clase abstracta Factura --------------------
class Factura(ABC):
    contador = 1

    def __init__(self, cliente):
        self.__numero = Factura.contador
        Factura.contador += 1
        self.__cliente = cliente
        self.__productos = []  # lista de tuplas (producto, cantidad)

    def get_numero(self)->int:
        return self.__numero

    def get_cliente(self)->str:
        return self.__cliente

    def get_productos(self)->str:
        return self.__productos

    def agregar_producto(self, producto:str, cantidad:int)->None:
        if producto.actualizar_stock(cantidad):
            self.__productos.append((producto, cantidad))
            print(f"✔ {cantidad} {producto.get_nombre()}(s) agregado(s) a la factura.")
        else:
            print(" Producto no disponible o stock insuficiente.")

    def calcular_total(self)->float:
        return sum(p.subtotal(c) for p, c in self.__productos)

    @abstractmethod
    def mostrar_factura(self):
        pass

    @abstractmethod
    def generar_pdf(self, nombre_archivo):
        pass


# -------------------- Factura Electrónica --------------------
class FacturaElectronica(Factura):
    def __init__(self, cliente, correo):
        super().__init__(cliente)
        self.__correo = correo

    def get_correo(self)->str:
        return self.__correo

    def mostrar_factura(self)->None:
        print(f"\nFactura Electrónica N° {self.get_numero()}")
        print(f"Cliente: {self.get_cliente().get_nombre()} - ID: {self.get_cliente().get_identificacion()}")
        print("Productos:")
        for p, cantidad in self.get_productos():
            print(f" - {p.get_nombre()} x{cantidad} - ${p.get_precio():.2f} c/u = ${p.subtotal(cantidad):.2f}")
        print(f"TOTAL: ${self.calcular_total():.2f}")
        print(f"Enviada a: {self.__correo}")

    def generar_pdf(self, nombre_archivo="factura_electronica.pdf")->None:
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        width, height = letter

        # -------------------- Encabezado --------------------
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 50, "FACTURA ELECTRÓNICA")

        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, height - 70, f"N° {self.get_numero()}")

        # -------------------- Datos del cliente --------------------
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 100, "Datos del Cliente:")
        c.setFont("Helvetica", 10)
        c.drawString(70, height - 115, f"Nombre: {self.get_cliente().get_nombre()}")
        c.drawString(70, height - 130, f"Identificación: {self.get_cliente().get_identificacion()}")
        c.drawString(70, height - 145, f"Correo: {self.__correo}")

        # -------------------- Tabla de productos --------------------
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 180, "Productos:")

        # Encabezados de tabla
        y = height - 200
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Producto")
        c.drawString(250, y, "Cantidad")
        c.drawString(350, y, "Precio")
        c.drawString(450, y, "Subtotal")
        c.line(45, y - 5, width - 45, y - 5)

        # Filas de productos
        y -= 20
        c.setFont("Helvetica", 10)
        for p, cantidad in self.get_productos():
            c.drawString(50, y, p.get_nombre())
            c.drawString(250, y, str(cantidad))
            c.drawString(350, y, f"${p.get_precio():.2f}")
            c.drawString(450, y, f"${p.subtotal(cantidad):.2f}")
            y -= 20

        # -------------------- Total --------------------
        c.line(300, y - 10, width - 45, y - 10)
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(width - 50, y - 30, f"TOTAL: ${self.calcular_total():.2f}")

        # -------------------- Footer --------------------
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(width / 2, 40, "Gracias por su compra ")

        # Guardar PDF
        c.save()


# -------------------- Sistema con Menú --------------------

def menu():
    inventario = Inventario()
    caja = Caja()
    facturas = []

    # Productos iniciales
    inventario.agregar_producto(Producto("Laptop", 3000, 5))
    inventario.agregar_producto(Producto("Mouse", 50, 20))
    inventario.agregar_producto(Producto("Teclado", 120, 10))

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Mostrar inventario")
        print("2. Agregar producto al inventario")
        print("3. Crear factura electrónica")
        print("4. Ver balance de caja")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inventario.mostrar_inventario()

        elif opcion == "2":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
            inventario.agregar_producto(Producto(nombre, precio, cantidad))
            print(f"✔ Producto {nombre} agregado al inventario.")

        elif opcion == "3":
            # Crear cliente
            nombre_cliente = input("Nombre del cliente: ")
            id_cliente = input("Identificación del cliente: ")
            correo = input("Correo del cliente: ")
            cliente = Cliente(nombre_cliente, id_cliente)

            factura = FacturaElectronica(cliente, correo)

            # Selección de productos
            while True:
                inventario.mostrar_inventario()
                producto_nombre = input("Ingrese producto (o 'fin' para terminar): ").lower()
                if producto_nombre == "fin":
                    break
                producto = inventario.buscar_producto(producto_nombre)
                if producto:
                    cantidad = int(input("Cantidad: "))
                    factura.agregar_producto(producto, cantidad)
                else:
                    print("Producto no encontrado en inventario.")

            # Mostrar y generar PDF
            if factura.get_productos():
                factura.mostrar_factura()
                factura.generar_pdf(f"factura_electronica_{factura.get_numero()}.pdf")
                caja.registrar_ingreso(factura.calcular_total())
                facturas.append(factura)
                print("📄 Factura electrónica generada con éxito.")
            else:
                print("No se generó factura (sin productos).")

        elif opcion == "4":
            print(f" Balance actual en caja: ${caja.balance():.2f}")

        elif opcion == "5":
            print("Saliendo del sistema...")
            break

        else:
            print(" Opción no válida, intente de nuevo.")


# -------------------- Ejecutar Menú --------------------
menu()
