# Juan dabid restrepo ocampo
# Santiago rico cardona

from abc import ABC, abstractmethod


#clase abstracta 
class MaterialBiblioteca(ABC):
    def __init__(self, titulo:str, autor:str, anio:int):
        self.__titulo = titulo
        self.__autor = autor
        self.__anio = anio
        self.__disponible = True

    def get_titulo(self)->str:
        return self.__titulo
    
    def set_titulo(self, titulo:str)->None:
        self.__titulo = titulo

    def get_autor(self)->str:
        return self.__autor
    
    def set_autor(self,autor)->None:
        self.__autor
        
    def get_anio(self)->int:
        return self.__anio
    
    def set_anio(self,anio:int)->None:
        self.__anio = anio

    def esta_disponible(self)->bool:
        return self.__disponible
    
    def set_disponible(self, disponible:bool)->bool:
        self.__disponible = disponible

    def prestar(self)->bool:
        if self.__disponible:
            self.__disponible = False
            return True
        return False

    def devolver(self):
        self.__disponible = True

    # Método abstracto 
    @abstractmethod
    def calcular_fecha_devolucion(self, dia_actual):
        pass

    @abstractmethod
    def obtener_detalles(self):
        pass


class Libro(MaterialBiblioteca):
    def __init__(self, titulo, autor, anio, genero):
        super().__init__(titulo, autor, anio)
        self.__genero = genero
    #polimorfismo
    def calcular_fecha_devolucion(self, dia_actual):
        return dia_actual + 15   

    def obtener_detalles(self):
        return f"[Libro] {self.get_titulo()} - {self.get_autor()} ({self.get_anio()}) - {self.__genero}"


class Revista(MaterialBiblioteca):
    def __init__(self, titulo, autor, anio, numero):
        super().__init__(titulo, autor, anio)
        self.__numero = numero

    def calcular_fecha_devolucion(self, dia_actual):
        return dia_actual + 7    # préstamo de 7 días

    def obtener_detalles(self):
        return f"[Revista] {self.get_titulo()} - {self.get_autor()} (N° {self.__numero}, {self.get_anio()})"


class MaterialAudiovisual(MaterialBiblioteca):
    def __init__(self, titulo, autor, anio, formato):
        super().__init__(titulo, autor, anio)
        self.__formato = formato

    def calcular_fecha_devolucion(self, dia_actual):
        return dia_actual + 3    # préstamo de 3 días

    def obtener_detalles(self):
        return f"[Audiovisual] {self.get_titulo()} - {self.get_autor()} ({self.get_anio()}) - {self.__formato}"

class Usuario:
    def __init__(self, nombre, cedula):
        self.__nombre = nombre
        self.__cedula = cedula
        self.__prestamos = []

    def prestar_material(self, material, dia_actual):
        if material.prestar():
            fecha_devolucion = material.calcular_fecha_devolucion(dia_actual)
            self.__prestamos.append((material, fecha_devolucion))
            print(f"{self.__nombre} ha prestado '{material.get_titulo()}'. Debe devolverlo en el día {fecha_devolucion}.")
        else:
            print(f"El material '{material.get_titulo()}' no está disponible.")

    def mostrar_prestamos(self):
        print(f"📚 Materiales prestados por {self.__nombre}:")
        for material, fecha in self.__prestamos:
            print(f"- {material.obtener_detalles()} | Fecha de devolución: día {fecha}")



if __name__ == "__main__":

    dia_actual = 100

    # Crear materiales
    libro1 = Libro("El Principito", "Antoine de Saint-Exupéry", 1943, "Fábula")
    revista1 = Revista("Scientific American", "Varios", 2024, 310)
    dvd1 = MaterialAudiovisual("Interstellar", "Christopher Nolan", 2014, "Blu-Ray")

    # Crear usuario
    usuario1 = Usuario("Juan Restrepo")

    # Usuario presta materiales
    usuario1.prestar_material(libro1, dia_actual)
    usuario1.prestar_material(revista1, dia_actual)
    usuario1.prestar_material(dvd1, dia_actual)

    # Mostrar préstamos
    usuario1.mostrar_prestamos()