# ============================================================
#  COLEGIO MARIANO MELGAR - REGISTRO DE INASISTENCIAS
# ============================================================
import os
import registro_matricula as matricula   # validaciones compartidas y datos de matrículas

ARCHIVO = "inasistencias.txt"
SIGNOS_MOTIVO = ",.;:()-¿?¡!/\"'"

# Arreglos paralelos: la posición i de cada lista pertenece a la misma inasistencia
codigos = []
estudiantes = []
fechas = []
motivos = []
estados = []
niveles = []
aulas = []
dnis_estudiantes = []


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def clave_fecha(fecha):
    """Convierte dd/mm/aaaa en aaaammdd para poder comparar fechas como texto."""
    dia, mes, anio = fecha.split("/")
    return anio + mes + dia


def validar_fecha(fecha):
    """Fecha real dd/mm/aaaa, desde hoy hasta el 31/12 del año actual."""
    if not matricula.validar_fecha_real(fecha):
        return False
    hoy = matricula.fecha_hoy()
    limite = "31/12/" + hoy[6:]
    return clave_fecha(hoy) <= clave_fecha(fecha) <= clave_fecha(limite)


def validar_motivo(motivo):
    """Al menos dos palabras y una letra; solo letras, números y signos habituales."""
    if len(motivo.split()) < 2:
        return False
    hay_letra = False
    for caracter in motivo:
        if caracter.isalpha():
            hay_letra = True
        elif not (caracter.isdigit() or caracter == " " or caracter in SIGNOS_MOTIVO):
            return False
    return hay_letra


def validar_si_no(respuesta):
    return respuesta.upper() in ("S", "N")


# ------------------------------------------------------------
# REGISTRO
# ------------------------------------------------------------
def registrar_inasistencia():
    """Pide los datos de la inasistencia, los valida y la guarda."""
    print("--- NUEVA INASISTENCIA ---")
    estudiante = matricula.pedir_dato("Nombre completo del estudiante: ",
                                      matricula.validar_nombre_completo,
                                      matricula.MENSAJE_NOMBRE)
    dni = matricula.pedir_dato("DNI del estudiante (8 dígitos): ", matricula.validar_dni,
                               "el DNI debe tener 8 dígitos numéricos.")
    nivel = matricula.pedir_nivel()
    aula = matricula.pedir_aula(nivel, "Grado y sección (ej. 3A): ")

    # Coherencia con el registro de matrículas (el DNI identifica al estudiante)
    posicion = matricula.buscar_por_dni(dni)
    if posicion != -1:
        if matricula.clave_busqueda(matricula.nombres[posicion]) != matricula.clave_busqueda(estudiante):
            print("  Error: el nombre no coincide con el del estudiante matriculado con ese DNI.")
            return
        nivel_igual = matricula.niveles[posicion] == nivel or matricula.niveles[posicion] == matricula.NIVEL_NO_DEFINIDO
        if not (nivel_igual and matricula.grados[posicion] + matricula.secciones[posicion] == aula):
            print("  Error: el nivel, grado o sección no coincide con la matrícula del estudiante.")
            return
        estudiante = matricula.nombres[posicion]

    hoy = matricula.fecha_hoy()
    fecha = matricula.pedir_dato("Fecha de la inasistencia (dd/mm/aaaa): ", validar_fecha,
                                 "ingrese una fecha real en formato dd/mm/aaaa, desde hoy (" + hoy + ").")
    motivo = matricula.pedir_dato("Motivo: ", validar_motivo,
                                  "el motivo debe tener al menos dos palabras, incluir letras y usar solo "
                                  "letras, números y signos como , . ( ) -")
    justificada = matricula.pedir_dato("¿Está justificada? (S/N): ", validar_si_no,
                                       "responda S o N.")

    if justificada.upper() == "S":
        estado = "Justificada"
    else:
        estado = "No justificada"

    codigo = matricula.generar_codigo("INA", len(codigos) + 1)
    codigos.append(codigo)
    estudiantes.append(matricula.normalizar_nombre(estudiante))
    fechas.append(fecha)
    motivos.append(" ".join(motivo.split()).capitalize())
    estados.append(estado)
    niveles.append(nivel)
    aulas.append(aula)
    dnis_estudiantes.append(dni)
    guardar_archivo()
    print("Inasistencia registrada con el código", codigo)
    if posicion == -1:
        print("  Aviso: el estudiante no figura en matrículas; no aparecerá en la consulta hasta que se matricule.")


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
    print("DNI        :", dnis_estudiantes[i])
    print("Nivel      :", niveles[i])
    print("Aula       :", aulas[i])
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


def contar_inasistencias(estudiante, dni):
    """Devuelve el total de inasistencias de un estudiante y cuántas están justificadas.
    Se une por DNI; los registros antiguos sin DNI se unen por nombre."""
    clave = matricula.clave_busqueda(estudiante)
    total = 0
    justificadas = 0
    for i in range(len(estudiantes)):
        coincide = dnis_estudiantes[i] == dni
        if dnis_estudiantes[i] == matricula.NO_REGISTRADO:
            coincide = matricula.clave_busqueda(estudiantes[i]) == clave
        if coincide:
            total = total + 1
            if estados[i] == "Justificada":
                justificadas = justificadas + 1
    return total, justificadas


def mostrar_resumen_estudiante(i):
    """Con el estudiante ya hallado en matrículas (posición i), muestra sus inasistencias."""
    print("Estudiante :", matricula.nombres[i])
    print("DNI        :", matricula.dnis[i])
    print("Nivel      :", matricula.niveles[i])
    print("Grado/Secc.:", matricula.grados[i] + matricula.secciones[i])
    total, justificadas = contar_inasistencias(matricula.nombres[i], matricula.dnis[i])
    if total == 0:
        print("Este estudiante no tiene inasistencias registradas")
    else:
        print("Total de inasistencias:", total)
        print("  Justificadas        :", justificadas)
        print("  No justificadas     :", total - justificadas)


def consultar_por_nombre():
    """Consulta de inasistencias identificando al estudiante por su nombre completo."""
    nombre = matricula.pedir_dato("Nombre completo del estudiante: ",
                                  matricula.validar_nombre_completo,
                                  matricula.MENSAJE_NOMBRE)
    posiciones = matricula.buscar_por_nombre(nombre)
    if len(posiciones) == 0:
        print("El estudiante no está registrado: no se encontró coincidencia con el nombre ingresado.")
    elif len(posiciones) > 1:
        print("Hay", len(posiciones), "estudiantes matriculados con ese nombre. Consulte por DNI.")
    else:
        mostrar_resumen_estudiante(posiciones[0])


def consultar_por_dni():
    """Consulta de inasistencias identificando al estudiante por su DNI."""
    dni = matricula.pedir_dato("DNI (8 dígitos): ", matricula.validar_dni,
                               "el DNI debe tener 8 dígitos numéricos.")
    i = matricula.buscar_por_dni(dni)
    if i == -1:
        print("El estudiante no está registrado: no se encontró coincidencia con el DNI ingresado.")
    else:
        mostrar_resumen_estudiante(i)


# ------------------------------------------------------------
# ORDENAMIENTO (selección, por fecha)
# ------------------------------------------------------------
def ordenar_por_fecha():
    n = len(codigos)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if clave_fecha(fechas[j]) < clave_fecha(fechas[menor]):
                menor = j
        if menor != i:
            for lista in (codigos, estudiantes, fechas, motivos, estados, niveles, aulas, dnis_estudiantes):
                lista[i], lista[menor] = lista[menor], lista[i]
    guardar_archivo()
    print("Inasistencias ordenadas por fecha.")


# ------------------------------------------------------------
# ARCHIVOS
# Formato: código|estudiante|fecha|motivo|estado|nivel|aula|dni
# ------------------------------------------------------------
def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            campos = [codigos[i], estudiantes[i], fechas[i], motivos[i], estados[i], niveles[i], aulas[i],
                      dnis_estudiantes[i]]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split("|")
            if len(campos) == 5 or len(campos) == 7 or len(campos) == 8:
                codigos.append(campos[0])
                estudiantes.append(campos[1])
                fechas.append(campos[2])
                motivos.append(campos[3])
                estados.append(campos[4])
                if len(campos) >= 7:
                    niveles.append(campos[5])
                    aulas.append(campos[6])
                else:
                    niveles.append(matricula.NIVEL_NO_DEFINIDO)
                    aulas.append(matricula.NIVEL_NO_DEFINIDO)
                if len(campos) == 8:
                    dnis_estudiantes.append(campos[7])
                else:
                    dnis_estudiantes.append(matricula.NO_REGISTRADO)
