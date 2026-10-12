# ============================================================
#   COLEGIO MARIANO MELGAR - SISTEMA DE MATRÍCULA
#   Versión con validaciones de datos
# ============================================================

# ------------------------------------------------------------
# >>> CAMBIO 1 (NUEVO): CONSTANTES DE APOYO
# Listas con los valores permitidos para nivel y grado.
# ------------------------------------------------------------
NIVELES = ["Inicial", "Primaria", "Secundaria"]

GRADOS_VALIDOS = {
    "Inicial": ["3", "4", "5"],            # edad en años
    "Primaria": ["1", "2", "3", "4", "5", "6"],
    "Secundaria": ["1", "2", "3", "4", "5"]
}

# ------------------------------------------------------------
# >>> CAMBIO 2 (NUEVO): FUNCIONES DE VALIDACIÓN
# Cada función recibe un texto y devuelve True si es válido
# o False si no lo es. No piden datos: solo revisan.
# ------------------------------------------------------------

# Valida nombres y apellidos: mínimo 2 palabras, solo letras
def validar_nombre_completo(texto):
    palabras = texto.split()
    if len(palabras) < 2:
        return False
    for palabra in palabras:
        # Permitimos apóstrofe y guion (ej.: D'Angelo, Pérez-Luna)
        letras = palabra.replace("'", "").replace("-", "")
        if len(letras) < 2 or not letras.isalpha():
            return False
    return True

# Valida DNI peruano: exactamente 8 dígitos
def validar_dni(texto):
    return len(texto) == 8 and texto.isdigit() and texto.isascii()

# Valida celular peruano: 9 dígitos y empieza con 9
def validar_celular(texto):
    return (len(texto) == 9 and texto.isdigit()
            and texto.isascii() and texto[0] == "9")

# Valida teléfono del trabajo: de 7 a 9 dígitos (fijo o celular)
def validar_telefono_trabajo(texto):
    return 7 <= len(texto) <= 9 and texto.isdigit() and texto.isascii()

# Valida dirección: mínimo 5 caracteres, al menos una letra
# y solo caracteres comunes en direcciones (letras, números,
# espacios y . , - # ° /)
def validar_direccion(texto):
    if len(texto) < 5:
        return False
    tiene_letra = False
    for caracter in texto:
        if caracter.isalpha():
            tiene_letra = True
        elif not (caracter.isdigit() or caracter in " .,-#°/"):
            return False
    return tiene_letra

# Valida correo: un solo @, sin espacios y con punto en el dominio
def validar_correo(texto):
    if " " in texto or texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return (len(usuario) > 0 and "." in dominio
            and not dominio.startswith(".")
            and not dominio.endswith("."))

# Valida sección: una sola letra
def validar_seccion(texto):
    return len(texto) == 1 and texto.isalpha()

# ------------------------------------------------------------
# >>> CAMBIO 3 (NUEVO): FUNCIÓN QUE PIDE UN DATO HASTA QUE
# SEA VÁLIDO
# Parámetros:
#   mensaje     -> texto que se muestra al usuario
#   validador   -> función de validación que se usará
#   error       -> mensaje si el dato es incorrecto
#   obligatorio -> si es False, se puede dejar vacío
# ------------------------------------------------------------
def pedir_dato(mensaje, validador, error, obligatorio=True):
    while True:
        valor = input(mensaje).strip()

        # Si el dato es opcional y se dejó vacío, se acepta
        if valor == "" and not obligatorio:
            return "No registra"

        # Si el dato es obligatorio, no se permite vacío
        if valor == "":
            print("  [!] Este dato es obligatorio. Intente nuevamente.")
        elif validador(valor):
            return valor
        else:
            print("  [!]", error)

# FUNCIÓN PARA REGISTRAR LOS DATOS DEL ESTUDIANTE
def registrar_estudiante():
    print("--------------------------------------")
    print("        DATOS DEL ESTUDIANTE")
    print("--------------------------------------")

    # >>> CAMBIO 4: ahora cada dato se pide con pedir_dato()
    # Solicitamos todos los datos del estudiante
    nombre_est = pedir_dato(
        "Nombre completo: ", validar_nombre_completo,
        "Ingrese nombres y apellidos (mínimo 2 palabras, solo letras)."
    ).title()

    dni_est = pedir_dato(
        "DNI: ", validar_dni,
        "El DNI debe tener exactamente 8 dígitos numéricos."
    )

    nivel = pedir_dato(
        "Nivel (Inicial/Primaria/Secundaria): ",
        lambda v: v.capitalize() in NIVELES,
        "Nivel no válido. Escriba Inicial, Primaria o Secundaria."
    ).capitalize()

    # El grado permitido depende del nivel elegido
    grado = pedir_dato(
        "Grado: ", lambda v: v in GRADOS_VALIDOS[nivel],
        "Grado no válido para " + nivel + ". Opciones: "
        + ", ".join(GRADOS_VALIDOS[nivel])
    )

    seccion = pedir_dato(
        "Sección: ", validar_seccion,
        "La sección debe ser una sola letra (ej.: A)."
    ).upper()

    # El celular del estudiante es opcional (puede ser menor)
    telefono_est = pedir_dato(
        "Teléfono (Enter si no tiene): ", validar_celular,
        "El celular debe tener 9 dígitos y empezar con 9.",
        obligatorio=False
    )

    correo_est = pedir_dato(
        "Correo (Enter si no tiene): ", validar_correo,
        "Correo no válido. Ejemplo: nombre@gmail.com",
        obligatorio=False
    )

    redes_est = input("Redes sociales: ").strip() or "No registra"

    direccion_est = pedir_dato(
        "Dirección: ", validar_direccion,
        "Dirección no válida (mínimo 5 caracteres, con letras). "
        "Ejemplo: Av. España 123"
    )

    urbanizacion_est = input("Urbanización: ").strip() or "No registra"

    colegio_anterior = input("Colegio anterior: ").strip() or "No registra"

    # Devolvemos todos los datos registrados
    return {
        "nombre": nombre_est,
        "dni": dni_est,
        "nivel": nivel,
        "grado": grado,
        "seccion": seccion,
        "telefono": telefono_est,
        "correo": correo_est,
        "redes": redes_est,
        "direccion": direccion_est,
        "urbanizacion": urbanizacion_est,
        "colegio_anterior": colegio_anterior
    }

# ------------------------------------------------------------
# FUNCIÓN PARA REGISTRAR LOS DATOS DE UN ADULTO
# Esta función se utiliza para registrar al padre, madre
# y apoderado, evitando repetir el mismo código tres veces.
# El parámetro "titulo" permite indicar qué adulto estamos
# registrando.
# ------------------------------------------------------------
def registrar_adulto(titulo):
    print("--------------------------------------")
    print("       ", titulo)
    print("--------------------------------------")

    # >>> CAMBIO 5: nombre, DNI, celular y dirección son
    # obligatorios y validados
    nombre = pedir_dato(
        "Nombre completo: ", validar_nombre_completo,
        "Ingrese nombres y apellidos (mínimo 2 palabras, solo letras)."
    ).title()

    dni = pedir_dato(
        "DNI: ", validar_dni,
        "El DNI debe tener exactamente 8 dígitos numéricos."
    )

    direccion = pedir_dato(
        "Dirección: ", validar_direccion,
        "Dirección no válida (mínimo 5 caracteres, con letras). "
        "Ejemplo: Av. España 123"
    )

    urbanizacion = input("Urbanización: ").strip() or "No registra"

    telefono = pedir_dato(
        "Celular: ", validar_celular,
        "El celular debe tener 9 dígitos, sin espacios, y empezar con 9."
    )

    correo = pedir_dato(
        "Correo (Enter si no tiene): ", validar_correo,
        "Correo no válido. Ejemplo: nombre@gmail.com",
        obligatorio=False
    )

    trabajo = input("Centro de trabajo: ").strip() or "No registra"

    cargo = input("Cargo: ").strip() or "No registra"

    telefono_trabajo = pedir_dato(
        "Teléfono del trabajo (Enter si no tiene): ",
        validar_telefono_trabajo,
        "Debe tener entre 7 y 9 dígitos numéricos.",
        obligatorio=False
    )

    # Guardamos todos los datos en un diccionario
    return {
        "nombre": nombre,
        "dni": dni,
        "direccion": direccion,
        "urbanizacion": urbanizacion,
        "telefono": telefono,
        "correo": correo,
        "trabajo": trabajo,
        "cargo": cargo,
        "telefono_trabajo": telefono_trabajo
    }

# ------------------------------------------------------------
# FUNCIÓN PARA MOSTRAR LOS DATOS DEL ESTUDIANTE
# ------------------------------------------------------------
def mostrar_estudiante(estudiante):
    print("--------------------------------------")
    print("        DATOS DEL ESTUDIANTE")
    print("--------------------------------------")
    print("Nombre          :", estudiante["nombre"])
    print("DNI             :", estudiante["dni"])
    print("Nivel           :", estudiante["nivel"])
    print("Grado / Sección :", estudiante["grado"], "/", estudiante["seccion"])
    print("Teléfono        :", estudiante["telefono"])
    print("Correo          :", estudiante["correo"])
    print("Redes sociales  :", estudiante["redes"])
    print("Dirección       :", estudiante["direccion"])
    print("Urbanización    :", estudiante["urbanizacion"])
    print("Colegio anterior:", estudiante["colegio_anterior"])

# ------------------------------------------------------------
# FUNCIÓN PARA MOSTRAR LOS DATOS DE UN ADULTO
# ------------------------------------------------------------
def mostrar_adulto(titulo, adulto):
    print("--------------------------------------")
    print("       ", titulo)
    print("--------------------------------------")
    print("Nombre          :", adulto["nombre"])
    print("DNI             :", adulto["dni"])
    print("Dirección       :", adulto["direccion"])
    print("Urbanización    :", adulto["urbanizacion"])
    print("Teléfono        :", adulto["telefono"])
    print("Correo          :", adulto["correo"])
    print("Centro trabajo  :", adulto["trabajo"])
    print("Cargo           :", adulto["cargo"])
    print("Teléf. trabajo  :", adulto["telefono_trabajo"])

# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------
# Al inicio no existe ninguna matrícula registrada.
registrado = False

# Variables donde se almacenarán los datos.
estudiante = None
padre = None
madre = None
apoderado = None

# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------
while True:
    print("======================================")
    print("       COLEGIO MARIANO MELGAR")
    print("       SISTEMA DE MATRÍCULA")
    print("======================================")
    print("1. Registrar matrícula")
    print("2. Mostrar datos registrados")
    print("3. Salir")

    # >>> CAMBIO 6: validamos la opción del menú. Antes, si el
    # usuario escribía una letra, el programa se cerraba con error.
    try:
        opcion = int(input("Seleccione una opción: "))
    except ValueError:
        print("  [!] Debe ingresar un número (1, 2 o 3).")
        print()
        continue

    # --------------------------------------------------------
    # OPCIÓN 1: REGISTRAR MATRÍCULA
    # --------------------------------------------------------
    if opcion == 1:
        # Registramos los datos del estudiante
        estudiante = registrar_estudiante()

        # Registramos los datos del padre
        padre = registrar_adulto("DATOS DEL PADRE")

        # Registramos los datos de la madre
        madre = registrar_adulto("DATOS DE LA MADRE")

        # Registramos los datos del apoderado
        apoderado = registrar_adulto("DATOS DEL APODERADO")

        # Indicamos que ya existe una matrícula registrada
        registrado = True

        print()
        print("Matrícula registrada correctamente.")
        print()

    # --------------------------------------------------------
    # OPCIÓN 2: MOSTRAR DATOS REGISTRADOS
    # --------------------------------------------------------
    elif opcion == 2:
        # Primero comprobamos si existe una matrícula
        if registrado:
            mostrar_estudiante(estudiante)
            mostrar_adulto("DATOS DEL PADRE", padre)
            mostrar_adulto("DATOS DE LA MADRE", madre)
            mostrar_adulto("DATOS DEL APODERADO", apoderado)
            print()
        else:
            print("No existen datos registrados.")
            print()

    # --------------------------------------------------------
    # OPCIÓN 3: SALIR DEL SISTEMA
    # --------------------------------------------------------
    elif opcion == 3:
        print("Gracias por utilizar el sistema.")
        break

    # --------------------------------------------------------
    # SI EL USUARIO INGRESA UNA OPCIÓN QUE NO EXISTE
    # --------------------------------------------------------
    else:
        print("Opción incorrecta.")
