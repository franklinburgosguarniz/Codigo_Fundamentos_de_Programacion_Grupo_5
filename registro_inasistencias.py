# ============================================================
#  COLEGIO MARIANO MELGAR - REGISTRO DE INASISTENCIAS
# ============================================================
import os

ARCHIVO = "inasistencias.txt"

# Arreglos paralelos: la posición i de cada lista pertenece a la misma inasistencia
codigos = []
estudiantes = []
fechas = []
motivos = []
estados = []


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def validar_texto(texto):
    """Devuelve True si el texto no está vacío y no usa el separador '|'."""
    return texto != "" and "|" not in texto


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


def validar_si_no(respuesta):
    return respuesta.upper() in ("S", "N")


# ------------------------------------------------------------
# CÓDIGO DE IDENTIFICACIÓN
# ------------------------------------------------------------
def generar_codigo(prefijo, numero):
    """Arma un código como INA-0001."""
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


def registrar_inasistencia():
    """Pide los datos de la inasistencia, los valida y la guarda."""
    print("--- NUEVA INASISTENCIA ---")
    estudiante = pedir_dato("Nombre completo del estudiante: ", validar_texto,
                            "el nombre no puede estar vacío ni contener '|'.")
    fecha = pedir_dato("Fecha de la inasistencia (dd/mm/aaaa): ", validar_fecha,
                       "use el formato dd/mm/aaaa con una fecha válida.")
    motivo = pedir_dato("Motivo: ", validar_texto,
                        "el motivo no puede estar vacío ni contener '|'.")
    justificada = pedir_dato("¿Está justificada? (S/N): ", validar_si_no,
                             "responda S o N.")

    if justificada.upper() == "S":
        estado = "Justificada"
    else:
        estado = "No justificada"

    codigo = generar_codigo("INA", len(codigos) + 1)
    codigos.append(codigo)
    estudiantes.append(" ".join(estudiante.split()).title())
    fechas.append(fecha)
    motivos.append(motivo.capitalize())
    estados.append(estado)
    guardar_archivo()
    print("Inasistencia registrada con el código", codigo)


# ------------------------------------------------------------
# CONSULTA
# ------------------------------------------------------------
def buscar_inasistencia(codigo):
    """Búsqueda secuencial por código. Devuelve la posición o -1."""
    codigo = codigo.strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == codigo:
            return i
    return -1


def mostrar_inasistencia(i):
    print("Código     :", codigos[i])
    print("Estudiante :", estudiantes[i])
    print("Fecha      :", fechas[i])
    print("Motivo     :", motivos[i])
    print("Estado     :", estados[i])
    print("-" * 40)


def mostrar_inasistencias():
    if len(codigos) == 0:
        print("No hay inasistencias registradas.")
        return
    for i in range(len(codigos)):
        mostrar_inasistencia(i)


def contar_inasistencias(estudiante):
    """Devuelve el total de inasistencias de un estudiante y cuántas están justificadas."""
    estudiante = " ".join(estudiante.split()).title()
    total = 0
    justificadas = 0
    for i in range(len(estudiantes)):
        if estudiantes[i] == estudiante:
            total = total + 1
            if estados[i] == "Justificada":
                justificadas = justificadas + 1
    return total, justificadas


# ------------------------------------------------------------
# ORDENAMIENTO (selección, por fecha)
# ------------------------------------------------------------
def clave_fecha(fecha):
    """Convierte dd/mm/aaaa en aaaammdd para poder comparar fechas como texto."""
    dia, mes, anio = fecha.split("/")
    return anio + mes + dia


def ordenar_por_fecha():
    n = len(codigos)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if clave_fecha(fechas[j]) < clave_fecha(fechas[menor]):
                menor = j
        if menor != i:
            for lista in (codigos, estudiantes, fechas, motivos, estados):
                lista[i], lista[menor] = lista[menor], lista[i]
    guardar_archivo()
    print("Inasistencias ordenadas por fecha.")


# ------------------------------------------------------------
# ARCHIVOS
# ------------------------------------------------------------
def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            campos = [codigos[i], estudiantes[i], fechas[i], motivos[i], estados[i]]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split("|")
            if len(campos) == 5:
                codigos.append(campos[0])
                estudiantes.append(campos[1])
                fechas.append(campos[2])
                motivos.append(campos[3])
                estados.append(campos[4])