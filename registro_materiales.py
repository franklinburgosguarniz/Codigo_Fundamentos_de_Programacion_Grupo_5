# ============================================================
#  COLEGIO MARIANO MELGAR - REGISTRO DE MATERIALES
# ============================================================
import os

ARCHIVO = "materiales.txt"

# Arreglos paralelos: la posición i de cada lista pertenece a la misma solicitud
codigos = []
docentes = []
aulas = []
materiales = []
cantidades = []
fechas = []


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def validar_texto(texto):
    """Devuelve True si el texto no está vacío y no usa el separador '|'."""
    return texto != "" and "|" not in texto


def validar_cantidad(cantidad):
    """La cantidad debe ser un número entero mayor que 0."""
    return cantidad.isdigit() and int(cantidad) > 0


def validar_fecha(fecha):
    """Formato dd/mm/aaaa con día 1-31 y mes 1-12."""
    partes = fecha.split("/")
    if len(partes) != 3:
        return False
    dia, mes, anio = partes
    if len(dia) != 2 or len(mes) != 2 or len(anio) != 4:
        return False
    if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
        return False
    return 1 <= int(dia) <= 31 and 1 <= int(mes) <= 12


# ------------------------------------------------------------
# CÓDIGO DE IDENTIFICACIÓN
# ------------------------------------------------------------
def generar_codigo(prefijo, numero):
    """Arma un código como MTR-0001."""
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


def registrar_material():
    """Pide los datos de la solicitud, los valida y la guarda."""
    print("--- NUEVA SOLICITUD DE MATERIAL ---")
    docente = pedir_dato("Nombre del docente: ", validar_texto,
                         "el nombre no puede estar vacío ni contener '|'.")
    aula = pedir_dato("Aula (ej. 3A): ", validar_texto,
                      "el aula no puede estar vacía ni contener '|'.")
    material = pedir_dato("Material solicitado (ej. Plumón, Recarga): ", validar_texto,
                          "el material no puede estar vacío ni contener '|'.")
    cantidad = pedir_dato("Cantidad: ", validar_cantidad,
                          "la cantidad debe ser un número entero mayor que 0.")
    fecha = pedir_dato("Fecha (dd/mm/aaaa): ", validar_fecha,
                       "use el formato dd/mm/aaaa con una fecha válida.")

    codigo = generar_codigo("MTR", len(codigos) + 1)
    codigos.append(codigo)
    docentes.append(" ".join(docente.split()).title())
    aulas.append(aula.upper())
    materiales.append(material.capitalize())
    cantidades.append(int(cantidad))
    fechas.append(fecha)
    guardar_archivo()
    print("Solicitud registrada con el código", codigo)


# ------------------------------------------------------------
# CONSULTA
# ------------------------------------------------------------
def buscar_material(codigo):
    """Búsqueda secuencial por código. Devuelve la posición o -1."""
    codigo = codigo.strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == codigo:
            return i
    return -1


def mostrar_material(i):
    print("Código   :", codigos[i])
    print("Docente  :", docentes[i])
    print("Aula     :", aulas[i])
    print("Material :", materiales[i])
    print("Cantidad :", cantidades[i])
    print("Fecha    :", fechas[i])
    print("-" * 40)


def mostrar_materiales():
    if len(codigos) == 0:
        print("No hay solicitudes registradas.")
        return
    for i in range(len(codigos)):
        mostrar_material(i)


def total_por_docente(docente):
    """Suma todas las cantidades entregadas a un docente."""
    docente = " ".join(docente.split()).title()
    total = 0
    for i in range(len(docentes)):
        if docentes[i] == docente:
            total = total + cantidades[i]
    return total


# ------------------------------------------------------------
# ARCHIVOS
# ------------------------------------------------------------
def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            campos = [codigos[i], docentes[i], aulas[i], materiales[i], str(cantidades[i]), fechas[i]]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split("|")
            if len(campos) == 6 and campos[4].isdigit():
                codigos.append(campos[0])
                docentes.append(campos[1])
                aulas.append(campos[2])
                materiales.append(campos[3])
                cantidades.append(int(campos[4]))
                fechas.append(campos[5])