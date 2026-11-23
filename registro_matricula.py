# ============================================================
#  COLEGIO MARIANO MELGAR - REGISTRO DE MATRÍCULA
#  (Este módulo también contiene las validaciones compartidas
#   que usan los registros de inasistencias y materiales)
# ============================================================
import os
from datetime import date

ARCHIVO = "matriculas.txt"

NIVELES = ["Primaria", "Secundaria"]
NIVEL_NO_DEFINIDO = "No definido"    
NO_REGISTRADO = "No registrado"      
LETRAS_SECCION = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MENSAJE_NOMBRE = ("ingrese al menos un nombre y dos apellidos, "
                  "usando solo letras y espacios (sin números ni símbolos).")

# Arreglos paralelos: la posición i de cada lista pertenece a la misma matrícula
codigos = []
nombres = []
dnis = []
grados = []
secciones = []
estados = []
niveles = []
contactos = []
direcciones = []
colegios_anteriores = []
fechas_matricula = []
# Cada familiar se guarda como lista: [nombre completo, DNI, contacto, dirección]
padres = []
madres = []
apoderados = []


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def es_numero(texto):
    """True si el texto tiene solo dígitos del 0 al 9 (y no está vacío)."""
    if texto == "":
        return False
    for caracter in texto:
        if caracter not in "0123456789":
            return False
    return True


def validar_nombre_completo(nombre):
    """Solo letras y espacios; mínimo un nombre y dos apellidos (3 palabras)."""
    if len(nombre.split()) < 3:
        return False
    for caracter in nombre:
        if not (caracter.isalpha() or caracter == " "):
            return False
    return True


def validar_dni(dni):
    """El DNI debe tener exactamente 8 dígitos."""
    return len(dni) == 8 and es_numero(dni)


def validar_contacto(contacto):
    """Celular: exactamente 9 dígitos y que empiece con 9."""
    return len(contacto) == 9 and es_numero(contacto) and contacto[0] == "9"


def validar_texto_obligatorio(texto):
    """Acepta letras, números y signos, pero no puede estar vacío ni llevar '|' (separador del TXT)."""
    return texto != "" and "|" not in texto


def validar_nivel(nivel):
    """Solo se acepta Primaria o Secundaria (sin importar mayúsculas)."""
    return nivel.capitalize() in NIVELES


def grado_maximo(nivel):
    """Primaria llega hasta 6.º grado; Secundaria hasta 5.º."""
    if nivel == "Primaria":
        return 6
    return 5


def validar_grado(grado, nivel):
    """El grado debe ser un número entero dentro del rango del nivel."""
    if not es_numero(grado) or grado != str(int(grado)):
        return False
    return 1 <= int(grado) <= grado_maximo(nivel)


def validar_seccion(seccion):
    """La sección es una sola letra (A, B, C...)."""
    return len(seccion) == 1 and seccion.upper() in LETRAS_SECCION


def validar_aula(aula, nivel):
    """Aula con formato número + letra (ej. 3A); el número depende del nivel."""
    if len(aula) < 2:
        return False
    return validar_grado(aula[:-1], nivel) and validar_seccion(aula[-1])


# ---------- Fechas (siempre se usa la fecha actual del sistema) ----------
def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0


def dias_del_mes(mes, anio):
    if mes == 2:
        if es_bisiesto(anio):
            return 29
        return 28
    if mes in (4, 6, 9, 11):
        return 30
    return 31


def validar_fecha_real(fecha):
    """Formato dd/mm/aaaa y que el día exista en el calendario."""
    partes = fecha.split("/")
    if len(partes) != 3:
        return False
    dia, mes, anio = partes
    if len(dia) != 2 or len(mes) != 2 or len(anio) != 4:
        return False
    if not (es_numero(dia) and es_numero(mes) and es_numero(anio)):
        return False
    if not 1 <= int(mes) <= 12:
        return False
    return 1 <= int(dia) <= dias_del_mes(int(mes), int(anio))


def fecha_hoy():
    """Fecha actual del sistema como dd/mm/aaaa."""
    hoy = date.today()
    return str(hoy.day).zfill(2) + "/" + str(hoy.month).zfill(2) + "/" + str(hoy.year)


def validar_fecha_hoy(fecha):
    """Solo se acepta la fecha de hoy (tomada del sistema)."""
    return fecha == fecha_hoy()


# ---------- Normalización de nombres ----------
def normalizar_nombre(nombre):
    """Sin espacios dobles y con mayúscula inicial en cada palabra."""
    return " ".join(nombre.split()).title()


def sin_tildes(texto):
    return texto.translate(str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU"))


def clave_busqueda(nombre):
    """Forma comparable de un nombre: sin tildes, sin espacios dobles y en minúscula."""
    return sin_tildes(" ".join(nombre.split()).lower())


# ------------------------------------------------------------
# CÓDIGO DE IDENTIFICACIÓN
# ------------------------------------------------------------
def generar_codigo(prefijo, numero):
    """Arma un código como MAT-0001."""
    return prefijo + "-" + str(numero).zfill(4)


# ------------------------------------------------------------
# ENTRADA DE DATOS (compartida por los tres registros)
# ------------------------------------------------------------
def pedir_dato(mensaje, validar, error):
    """Repite la pregunta hasta que el dato sea válido y lo devuelve limpio."""
    dato = input(mensaje).strip()
    while not validar(dato):
        print("  Error:", error)
        dato = input(mensaje).strip()
    return dato


def pedir_nivel():
    """Pide el nivel educativo y lo devuelve como 'Primaria' o 'Secundaria'."""
    nivel = pedir_dato("Nivel educativo (Primaria/Secundaria): ", validar_nivel,
                       "el nivel debe ser Primaria o Secundaria.")
    return nivel.capitalize()


def pedir_grado(nivel):
    """Pide el grado, que depende del nivel ya seleccionado."""
    maximo = str(grado_maximo(nivel))
    mensaje = "Grado de " + nivel + " (1 a " + maximo + "): "
    grado = input(mensaje).strip()
    while not validar_grado(grado, nivel):
        print("  Error: en " + nivel + " el grado debe ser un número entero del 1 al " + maximo + ".")
        grado = input(mensaje).strip()
    return grado


def pedir_aula(nivel, mensaje="Aula y sección (ej. 3A): "):
    """Pide grado y sección juntos, con formato número + letra (ej. 3A).
    El número permitido depende del nivel."""
    maximo = str(grado_maximo(nivel))
    error = ("escriba el grado y la sección juntos: un número del 1 al " + maximo + " de " + nivel +
             " seguido de una letra, por ejemplo 3A.")
    aula = input(mensaje).strip().upper()
    while not validar_aula(aula, nivel):
        print("  Error:", error)
        aula = input(mensaje).strip().upper()
    return aula


# ------------------------------------------------------------
# REGISTRO
# ------------------------------------------------------------
MENSAJE_TEXTO = "este dato es obligatorio: no puede quedar vacío ni contener el signo |."
MENSAJE_CONTACTO = "el contacto debe tener 9 dígitos numéricos y empezar con 9 (sin letras ni signos)."


def pedir_datos_familiar(parentesco):
    """Pide nombre completo, DNI, contacto y dirección del padre, la madre o el apoderado."""
    print("--- Datos de la madre ---" if parentesco == "madre" else "--- Datos del " + parentesco + " ---")
    nombre = pedir_dato("Nombre completo (" + parentesco + "): ", validar_nombre_completo, MENSAJE_NOMBRE)
    dni = pedir_dato("DNI (" + parentesco + ", 8 dígitos): ", validar_dni,
                     "el DNI debe tener 8 dígitos numéricos.")
    contacto = pedir_dato("Contacto (" + parentesco + ", 9 dígitos): ", validar_contacto, MENSAJE_CONTACTO)
    direccion = pedir_dato("Dirección (" + parentesco + "): ", validar_texto_obligatorio, MENSAJE_TEXTO)
    return [normalizar_nombre(nombre), dni, contacto, direccion]


def registrar_matricula():
    """Pide los datos del estudiante y de su familia, los valida y guarda la matrícula."""
    print("--- NUEVA MATRÍCULA ---")
    nombre = pedir_dato("Nombre completo del estudiante: ", validar_nombre_completo,
                        MENSAJE_NOMBRE)
    dni = pedir_dato("DNI (8 dígitos): ", validar_dni,
                     "el DNI debe tener 8 dígitos numéricos.")
    # Evitamos matricular dos veces al mismo DNI
    if dni in dnis:
        print("  Error: ya existe una matrícula con ese DNI.")
        return
    nivel = pedir_nivel()
    grado = pedir_grado(nivel)
    seccion = pedir_dato("Sección (una letra): ", validar_seccion,
                         "la sección debe ser una sola letra (A, B, C...).")
    contacto = pedir_dato("Contacto del estudiante (9 dígitos): ", validar_contacto, MENSAJE_CONTACTO)
    direccion = pedir_dato("Dirección del estudiante: ", validar_texto_obligatorio, MENSAJE_TEXTO)
    colegio = pedir_dato("Colegio anterior: ", validar_texto_obligatorio, MENSAJE_TEXTO)
    padre = pedir_datos_familiar("padre")
    madre = pedir_datos_familiar("madre")
    apoderado = pedir_datos_familiar("apoderado")
    hoy = fecha_hoy()
    fecha = pedir_dato("Fecha de matrícula (" + hoy + "): ", validar_fecha_hoy,
                       "la fecha debe ser la de hoy (" + hoy + "), no una anterior ni futura.")

    codigo = generar_codigo("MAT", len(codigos) + 1)
    codigos.append(codigo)
    nombres.append(normalizar_nombre(nombre))
    dnis.append(dni)
    niveles.append(nivel)
    grados.append(grado)
    secciones.append(seccion.upper())
    estados.append("Pendiente")
    contactos.append(contacto)
    direcciones.append(direccion)
    colegios_anteriores.append(colegio)
    fechas_matricula.append(fecha)
    padres.append(padre)
    madres.append(madre)
    apoderados.append(apoderado)
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


def buscar_por_dni(dni):
    """Búsqueda secuencial por DNI. Devuelve la posición o -1."""
    for i in range(len(dnis)):
        if dnis[i] == dni:
            return i
    return -1


def buscar_por_nombre(nombre):
    """Devuelve la lista de posiciones cuyo nombre coincide (puede haber homónimos)."""
    clave = clave_busqueda(nombre)
    posiciones = []
    for i in range(len(nombres)):
        if clave_busqueda(nombres[i]) == clave:
            posiciones.append(i)
    return posiciones


def mostrar_familiar(titulo, datos):
    print(titulo + ":", datos[0], "| DNI:", datos[1], "| Contacto:", datos[2])
    print("    Dirección:", datos[3])


def mostrar_matricula(i):
    print("Código    :", codigos[i])
    print("Nombre    :", nombres[i])
    print("DNI       :", dnis[i])
    print("Nivel     :", niveles[i])
    print("Grado     :", grados[i], "-", secciones[i])
    print("Contacto  :", contactos[i])
    print("Dirección :", direcciones[i])
    print("Colegio anterior:", colegios_anteriores[i])
    mostrar_familiar("Padre", padres[i])
    mostrar_familiar("Madre", madres[i])
    mostrar_familiar("Apoderado", apoderados[i])
    print("Fecha de matrícula:", fechas_matricula[i])
    print("Estado    :", estados[i])
    print("-" * 40)


def mostrar_matriculas():
    if len(codigos) == 0:
        print("No hay matrículas registradas.")
        return
    for i in range(len(codigos)):
        mostrar_matricula(i)


def mostrar_pendientes():
    """Muestra únicamente las matrículas con estado 'Pendiente'."""
    cantidad = 0
    for i in range(len(codigos)):
        if estados[i] == "Pendiente":
            mostrar_matricula(i)
            cantidad = cantidad + 1
    if cantidad == 0:
        print("No hay matrículas pendientes.")


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
# ORDENAMIENTO (selección, por apellido)
# ------------------------------------------------------------
def obtener_apellidos(nombre):
    """Los apellidos son las dos últimas palabras del nombre completo."""
    palabras = nombre.split()
    if len(palabras) >= 3:
        return " ".join(palabras[-2:])
    return " ".join(palabras[-1:])      # registros antiguos con menos palabras


def clave_apellido(nombre):
    """Texto para ordenar: primero los apellidos y luego los nombres."""
    apellidos = obtener_apellidos(nombre)
    nombres_pila = nombre[:len(nombre) - len(apellidos)]
    return sin_tildes((apellidos + " " + nombres_pila).lower())


def ordenar_por_apellido():
    n = len(codigos)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if clave_apellido(nombres[j]) < clave_apellido(nombres[menor]):
                menor = j
        if menor != i:
            # Se intercambian todos los arreglos para no separar los datos
            for lista in (codigos, nombres, dnis, grados, secciones, estados, niveles, contactos,
                          direcciones, colegios_anteriores, fechas_matricula, padres, madres, apoderados):
                lista[i], lista[menor] = lista[menor], lista[i]
    guardar_archivo()
    print("Matrículas ordenadas por apellido.")


# ------------------------------------------------------------
# ARCHIVOS
# Formato (23 campos): código|nombre|dni|grado|sección|estado|nivel|contacto|dirección|
#   colegio anterior|fecha|padre (4 campos)|madre (4 campos)|apoderado (4 campos)
# Cada familiar: nombre|dni|contacto|dirección
# ------------------------------------------------------------
def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            campos = [codigos[i], nombres[i], dnis[i], grados[i], secciones[i], estados[i], niveles[i],
                      contactos[i], direcciones[i], colegios_anteriores[i], fechas_matricula[i]]
            campos = campos + padres[i] + madres[i] + apoderados[i]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split("|")
            if len(campos) == 6 or len(campos) == 7 or len(campos) == 23:
                codigos.append(campos[0])
                nombres.append(campos[1])
                dnis.append(campos[2])
                grados.append(campos[3])
                secciones.append(campos[4])
                estados.append(campos[5])
                if len(campos) >= 7:
                    niveles.append(campos[6])
                else:
                    niveles.append(NIVEL_NO_DEFINIDO)
                if len(campos) == 23:
                    contactos.append(campos[7])
                    direcciones.append(campos[8])
                    colegios_anteriores.append(campos[9])
                    fechas_matricula.append(campos[10])
                    padres.append(campos[11:15])
                    madres.append(campos[15:19])
                    apoderados.append(campos[19:23])
                else:
                    contactos.append(NO_REGISTRADO)
                    direcciones.append(NO_REGISTRADO)
                    colegios_anteriores.append(NO_REGISTRADO)
                    fechas_matricula.append(NO_REGISTRADO)
                    padres.append([NO_REGISTRADO] * 4)
                    madres.append([NO_REGISTRADO] * 4)
                    apoderados.append([NO_REGISTRADO] * 4)
