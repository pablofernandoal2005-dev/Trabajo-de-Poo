#Trabajo Grupal de Pooll
#Diana Tigre, Maria Bravo, Daniela Corte, Steven Ortiz, Pablo Alvarado

from datetime import date


class LibroNoExisteError(Exception):
    pass

class LibroNoDisponibleError(Exception):
    pass

class LibroNoPrestadoError(Exception):
    pass

class CampoVacioError(Exception):
    pass

class Libro:
    def __init__(self, codigo, titulo, autor, estado="Disponible"):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.estado = estado

    def prestar(self):
        if self.estado != "Disponible":
            raise LibroNoDisponibleError("el libro ya esta prestado")
        self.estado = "Prestado"

    def devolver(self):
        if self.estado != "Prestado":
            raise LibroNoPrestadoError("el libro no esta prestado")
        self.estado = "Disponible"

    def __str__(self):
        return f"Codigo: {self.codigo}\nTitulo: {self.titulo}\nAutor: {self.autor}\nEstado: {self.estado}"

class Prestamo:
    def __init__(self, numero, codigo, estudiante, fecha, estado="Activo"):
        self.numero = numero
        self.codigo = codigo
        self.estudiante = estudiante
        self.fecha = fecha
        self.estado = estado

    def devolver(self):
        self.estado = "Devuelto"

libro_iniciales = [
    Libro(1, "Cien años de soledad", "Gabriel Garcia Marquez"),
    Libro(2, "Don Quijote de la mancha", "Miguel de Cervantes"),
    Libro(3, "Orgullo y Prejuicio", "Jane Austen"),
    Libro(4, "El Señor de los Anillos", "J.R.R. Tolkien"),
    Libro(5, "La Divina Comedia", "Dante Alighieri")
]

try:
    with open("Libros.txt", "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    contenido = ""

if contenido.strip() == "":
    with open("Libros.txt", "w", encoding="utf-8") as archivo:
        for libro in libro_iniciales:
            archivo.write(f"{libro.codigo},{libro.titulo},{libro.autor},{libro.estado}\n")

try:
    with open("Prestamos.txt", "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    with open("Prestamos.txt", "w", encoding="utf-8") as archivo:
        archivo.write("")


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error, debe ingresar un numero entero")


def buscar_por_codigo(libros, codigo):
    for libro in libros:
        if libro.codigo == codigo:
            return libro
    raise LibroNoExisteError("el codigo del libro no existe")


def cargar_libros():
    libros = []
    try:
        with open("Libros.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() == "":
                    continue
                datos = linea.strip().split(",")
                libros.append(Libro(int(datos[0]), datos[1], datos[2], datos[3]))
    except FileNotFoundError:
        pass
    return libros

def cargar_prestamos():
    prestamos = []
    try:
        with open("Prestamos.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() == "":
                    continue
                datos = linea.strip().split(",")
                prestamos.append(Prestamo(int(datos[0]), int(datos[1]), datos[2], datos[3], datos[4]))
    except FileNotFoundError:
        pass
    return prestamos

def guardar_libros(libros):
    with open("Libros.txt", "w", encoding="utf-8") as archivo:
        for l in libros:
            archivo.write(f"{l.codigo},{l.titulo},{l.autor},{l.estado}\n")


def guardar_prestamos(prestamos):
    with open("Prestamos.txt", "w", encoding="utf-8") as archivo:
        for p in prestamos:
            archivo.write(f"{p.numero},{p.codigo},{p.estudiante},{p.fecha},{p.estado}\n")

def registrar_libros(libros):
    titulo = input("Ingrese el titulo del libro: ").strip()
    autor = input("Ingrese el autor del libro: ").strip()

    if titulo == "" or autor == "":
        raise CampoVacioError("no se aceptan campos vacios")
    if "," in titulo or "," in autor:
        raise ValueError("no se permiten comas")

    if len(libros) > 0:
        codigo = libros[-1].codigo + 1
    else:
        codigo = 1

    libro = Libro(codigo, titulo, autor)
    libros.append(libro)
    guardar_libros(libros)
    print("Libro registrado correctamente")
    return libro

def mostrar_libros(libros):
    print("========== LISTA DE LIBROS ===========")
    for libro in libros:
        print(libro)
        print("======================================")
    return len(libros)

def buscar_libro(libros):
    palabra = input("Ingrese la palabra a buscar: ").strip()
    if palabra == "":
        raise CampoVacioError("no se acepta un texto vacio")

    encontrados = 0
    print("\n========== RESULTADO DE BUSQUEDA ===========")
    print(f"{'Codigo':<8}{'Titulo':<30}{'Autor':<25}{'Estado':<12}")
    print("-" * 75)
    for l in libros:
        if palabra.lower() in l.titulo.lower():
            print(f"{l.codigo:<8}{l.titulo:<30}{l.autor:<25}{l.estado:<12}")
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron libros con esa palabra")
    return encontrados

def prestar_libro(libros, prestamos):
    codigo = leer_entero("Ingrese el codigo del libro: ")
    libro = buscar_por_codigo(libros, codigo)
    libro.prestar()

    estudiante = input("Ingrese el nombre del estudiante: ").strip()
    if estudiante == "":
        raise CampoVacioError("el nombre no puede estar vacio")

    fecha = str(date.today())

    if len(prestamos) > 0:
        numero = prestamos[-1].numero + 1
    else:
        numero = 1

    prestamos.append(Prestamo(numero, codigo, estudiante, fecha))
    print("Libro prestado correctamente")
    return True

def devolver_libro(libros, prestamos):
    codigo = leer_entero("Ingrese el codigo del libro: ")
    libro = buscar_por_codigo(libros, codigo)
    libro.devolver()

    for p in prestamos:
        if p.codigo == codigo and p.estado == "Activo":
            p.devolver()
            break
    print("Libro devuelto correctamente")
    return True

def mostrar_prestamos(prestamos, libros):
    print("\n========== LISTA DE PRESTAMOS ===========")
    print(f"{'N°':<5}{'Libro':<30}{'Estudiante':<22}{'Fecha':<13}{'Estado':<10}")
    print("-" * 80)
    for p in prestamos:
        try:
            titulo = buscar_por_codigo(libros, p.codigo).titulo
        except LibroNoExisteError:
            titulo = "(desconocido)"
        print(f"{p.numero:<5}{titulo:<30}{p.estudiante:<22}{p.fecha:<13}{p.estado:<10}")
    if len(prestamos) == 0:
        print("No hay prestamos registrados")
    return len(prestamos)

def reporte_general(libros, prestamos):
    total = len(libros)
    disponibles = sum(1 for l in libros if l.estado == "Disponible")
    prestados = sum(1 for l in libros if l.estado == "Prestado")
    activos = sum(1 for p in prestamos if p.estado == "Activo")

    try:
        porcentaje = (prestados / total) * 100
    except ZeroDivisionError:
        porcentaje = 0

    print("\n========== REPORTE GENERAL ==========")
    print(f"Total de libros:        {total}")
    print(f"Libros disponibles:     {disponibles}")
    print(f"Libros prestados:       {prestados}")
    print(f"Prestamos activos:      {activos}")
    print(f"Porcentaje prestados:   {porcentaje:.2f}%")
    return porcentaje
opcion = 0
while opcion != 8:

    print("======================================")
    print("   BIBLIOTECA DIGITAL DEL TEC AZUAY   ")
    print("======================================")
    print("1. Registrar Libro")
    print("2. Mostrar libros")
    print("3. Buscar libro")
    print("4. Prestar libro")
    print("5. Devolver libro")
    print("6. Mostrar prestamos")
    print("7. Reporte general")
    print("8. Salir")

    opcion = leer_entero("Ingrese una opcion a elegir: ")
    try:
        if opcion == 1:
            registrar_libros(cargar_libros())

        elif opcion == 2:
            mostrar_libros(cargar_libros())

        elif opcion == 3:
            buscar_libro(cargar_libros())

        elif opcion == 4:
            libros = cargar_libros()
            prestamos = cargar_prestamos()
            prestar_libro(libros, prestamos)
            guardar_libros(libros)
            guardar_prestamos(prestamos)

        elif opcion == 5:
            libros = cargar_libros()
            prestamos = cargar_prestamos()
            devolver_libro(libros, prestamos)
            guardar_libros(libros)
            guardar_prestamos(prestamos)
        elif opcion == 6:
            mostrar_prestamos(cargar_prestamos(), cargar_libros())
        elif opcion == 7:
            reporte_general(cargar_libros(), cargar_prestamos())
        elif opcion == 8:
            print("Gracias por utilizar la biblioteca")
        else:
            print("Debe de ingresar un numero valido entre 1 al 8")

    except (LibroNoExisteError, LibroNoDisponibleError, LibroNoPrestadoError) as e:
        print("Error:", e)
    except CampoVacioError as e:
        print("Error:", e)
    except ValueError as e:
        print("Error:", e)
    finally:
        print()