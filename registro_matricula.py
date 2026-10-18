# ============================================================
#  COLEGIO MARIANO MELGAR - REGISTRO DE MATRÍCULA
# ============================================================
import os

ARCHIVO = "matriculas.txt"

# Arreglos paralelos: la posición i de cada lista pertenece a la misma matrícula
codigos = []
nombres = []
dnis = []
grados = []
secciones = []
estados = []


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def validar_texto(texto):
    """Devuelve True si el texto no está vacío y no usa el separador '|'."""
    return texto != "" and "|" not in texto


def validar_dni(dni):
    """El DNI debe tener exactamente 8 dígitos."""
    return len(dni) == 8 and dni.isdigit()


def validar_grado(grado):
    """El grado debe ser un número del 1 al 6."""
    return grado.isdigit() and 1 <= int(grado) <= 6


def validar_seccion(seccion):
    """La sección es una sola letra (A, B, C...)."""
    return len(seccion) == 1 and seccion.isalpha()


# ------------------------------------------------------------
# CÓDIGO DE IDENTIFICACIÓN
# ------------------------------------------------------------
def generar_codigo(prefijo, numero):
    """Arma un código como MAT-0001."""
    return prefijo + "-" + str(numero).zfill(4)


# ------------------------------------------------------------
# REGISTRO
# ------------------------------------------------------------
def pedir_dato(mensaje, validar, error):
    """Repite la pregunta hasta que el dato sea válido y lo devuelve limpio."""
    dato = input(mensaje).strip()
    while not validar(dato):
        print("  Error:", error)
        dato = input(mensaje).strip()
    return dato


def registrar_matricula():
    """Pide los datos del estudiante, los valida y guarda la matrícula."""
    print("--- NUEVA MATRÍCULA ---")
    nombre = pedir_dato("Nombre completo del estudiante: ", validar_texto,
                        "el nombre no puede estar vacío ni contener '|'.")
    dni = pedir_dato("DNI (8 dígitos): ", validar_dni,
                     "el DNI debe tener 8 dígitos numéricos.")
    # Evitamos matricular dos veces al mismo DNI
    if dni in dnis:
        print("  Error: ya existe una matrícula con ese DNI.")
        return
    grado = pedir_dato("Grado (1 a 6): ", validar_grado,
                       "el grado debe ser un número del 1 al 6.")
    seccion = pedir_dato("Sección (una letra): ", validar_seccion,
                         "la sección debe ser una sola letra.")

    codigo = generar_codigo("MAT", len(codigos) + 1)
    codigos.append(codigo)
    nombres.append(" ".join(nombre.split()).title())   # sin espacios dobles y con mayúscula inicial
    dnis.append(dni)
    grados.append(grado)
    secciones.append(seccion.upper())
    estados.append("Pendiente")
    guardar_archivo()
    print("Matrícula registrada con el código", codigo)


# ------------------------------------------------------------
# CONSULTA
# ------------------------------------------------------------
def buscar_matricula(codigo):
    """Búsqueda secuencial por código. Devuelve la posición o -1."""
    codigo = codigo.strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == codigo:
            return i
    return -1


def mostrar_matricula(i):
    print("Código  :", codigos[i])
    print("Nombre  :", nombres[i])
    print("DNI     :", dnis[i])
    print("Grado   :", grados[i], "-", secciones[i])
    print("Estado  :", estados[i])
    print("-" * 40)


def mostrar_matriculas():
    if len(codigos) == 0:
        print("No hay matrículas registradas.")
        return
    for i in range(len(codigos)):
        mostrar_matricula(i)


def confirmar_matricula(codigo):
    """Cambia el estado de la matrícula a 'Matriculado'."""
    i = buscar_matricula(codigo)
    if i == -1:
        print("No se encontró la matrícula.")
    else:
        estados[i] = "Matriculado"
        guardar_archivo()
        print("La matrícula", codigos[i], "ahora está 'Matriculado'.")


# ------------------------------------------------------------
# ORDENAMIENTO (selección, por nombre)
# ------------------------------------------------------------
def ordenar_por_nombre():
    n = len(codigos)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if nombres[j] < nombres[menor]:
                menor = j
        if menor != i:
            # Se intercambian todos los arreglos para no separar los datos
            for lista in (codigos, nombres, dnis, grados, secciones, estados):
                lista[i], lista[menor] = lista[menor], lista[i]
    guardar_archivo()
    print("Matrículas ordenadas por nombre.")


# ------------------------------------------------------------
# ARCHIVOS
# ------------------------------------------------------------
def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            campos = [codigos[i], nombres[i], dnis[i], grados[i], secciones[i], estados[i]]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split("|")
            if len(campos) == 6:
                codigos.append(campos[0])
                nombres.append(campos[1])
                dnis.append(campos[2])
                grados.append(campos[3])
                secciones.append(campos[4])
                estados.append(campos[5])