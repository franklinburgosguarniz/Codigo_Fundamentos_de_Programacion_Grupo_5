# ============================================================
#  COLEGIO MARIANO MELGAR - REGISTRO DE MATERIALES
# ============================================================
import os
import registro_matricula as matricula   # validaciones compartidas (nombre, nivel, aula, fecha)

ARCHIVO = "materiales.txt"

# Arreglos paralelos: la posición i de cada lista pertenece a la misma solicitud
codigos = []
docentes = []
aulas = []
materiales = []
cantidades = []
fechas = []
niveles = []


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def validar_material(texto):
    """Solo letras y espacios; las comas separan materiales y ninguno puede quedar vacío."""
    for caracter in texto:
        if not (caracter.isalpha() or caracter == " " or caracter == ","):
            return False
    for parte in texto.split(","):
        if parte.strip() == "":
            return False
    return True


def validar_cantidad(cantidad):
    """La cantidad debe ser un número entero mayor que 0."""
    return matricula.es_numero(cantidad) and int(cantidad) > 0


# ------------------------------------------------------------
# REGISTRO
# ------------------------------------------------------------
def registrar_material():
    """Pide los datos de la solicitud, los valida y la guarda."""
    print("--- NUEVA SOLICITUD DE MATERIAL ---")
    docente = matricula.pedir_dato("Nombre completo del docente: ",
                                   matricula.validar_nombre_completo,
                                   matricula.MENSAJE_NOMBRE)
    nivel = matricula.pedir_nivel()
    aula = matricula.pedir_aula(nivel)
    material = matricula.pedir_dato("Material solicitado (ej. Plumón, Recarga): ", validar_material,
                                    "escriba los materiales solo con letras y espacios, separados por comas "
                                    "(sin números ni otros símbolos).")
    cantidad = matricula.pedir_dato("Cantidad: ", validar_cantidad,
                                    "la cantidad debe ser un número entero mayor que 0.")
    hoy = matricula.fecha_hoy()
    fecha = matricula.pedir_dato("Fecha de solicitud (" + hoy + "): ", matricula.validar_fecha_hoy,
                                 "la fecha debe ser la de hoy (" + hoy + "), no una anterior ni futura.")

    # Se guardan los materiales separados por ", " y sin espacios sobrantes
    lista_materiales = []
    for parte in material.split(","):
        lista_materiales.append(" ".join(parte.split()))

    codigo = matricula.generar_codigo("MTR", len(codigos) + 1)
    codigos.append(codigo)
    docentes.append(matricula.normalizar_nombre(docente))
    niveles.append(nivel)
    aulas.append(aula)
    materiales.append(", ".join(lista_materiales).capitalize())
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
    print("Nivel    :", niveles[i])
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
    clave = matricula.clave_busqueda(docente)
    total = 0
    for i in range(len(docentes)):
        if matricula.clave_busqueda(docentes[i]) == clave:
            total = total + cantidades[i]
    return total


def consultar_total_docente():
    """Pide el nombre completo del docente (validado) y muestra el total entregado."""
    docente = matricula.pedir_dato("Nombre completo del docente: ",
                                   matricula.validar_nombre_completo,
                                   matricula.MENSAJE_NOMBRE)
    print("Total entregado:", total_por_docente(docente))


# ------------------------------------------------------------
# ARCHIVOS
# Formato: código|docente|aula|material|cantidad|fecha|nivel
# ------------------------------------------------------------
def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            campos = [codigos[i], docentes[i], aulas[i], materiales[i], str(cantidades[i]), fechas[i], niveles[i]]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split("|")
            if (len(campos) == 6 or len(campos) == 7) and campos[4].isdigit():
                codigos.append(campos[0])
                docentes.append(campos[1])
                aulas.append(campos[2])
                materiales.append(campos[3])
                cantidades.append(int(campos[4]))
                fechas.append(campos[5])
                if len(campos) == 7:
                    niveles.append(campos[6])
                else:
                    niveles.append(matricula.NIVEL_NO_DEFINIDO)
