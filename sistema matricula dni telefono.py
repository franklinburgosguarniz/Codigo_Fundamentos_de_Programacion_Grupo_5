# ============================================================
#   COLEGIO MARIANO MELGAR - SISTEMA DE MATRÍCULA
# ============================================================

# ------------------------------------------------------------
# >>> NUEVO: FUNCIÓN QUE PIDE EL DNI Y LO VALIDA
# El DNI debe tener exactamente 8 dígitos numéricos.
# Repite la pregunta hasta que el dato sea correcto.
# ------------------------------------------------------------
def pedir_dni():
    while True:
        dni = input("DNI: ").strip()
        if len(dni) == 8 and dni.isdigit():
            return dni
        print("  [!] El DNI debe tener exactamente 8 dígitos numéricos.")

# ------------------------------------------------------------
# >>> NUEVO: FUNCIÓN QUE PIDE UN TELÉFONO Y LO VALIDA
# El celular debe tener 9 dígitos y empezar con 9.
# El parámetro "mensaje" permite reutilizar la función.
# ------------------------------------------------------------
def pedir_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        if len(telefono) == 9 and telefono.isdigit() and telefono[0] == "9":
            return telefono
        print("  [!] El teléfono debe tener 9 dígitos y empezar con 9.")

# FUNCIÓN PARA REGISTRAR LOS DATOS DEL ESTUDIANTE
def registrar_estudiante():
    print("--------------------------------------")
    print("        DATOS DEL ESTUDIANTE")
    print("--------------------------------------")

    # Solicitamos todos los datos del estudiante
    nombre_est = input("Nombre completo: ")

    # >>> CAMBIO: antes era input("DNI: ")
    dni_est = pedir_dni()

    nivel = input("Nivel (Inicial/Primaria/Secundaria): ")

    grado = input("Grado: ")

    seccion = input("Sección: ")

    # >>> CAMBIO: antes era input("Teléfono: ")
    telefono_est = pedir_telefono("Teléfono: ")

    correo_est = input("Correo: ")

    redes_est = input("Redes sociales: ")

    direccion_est = input("Dirección: ")

    urbanizacion_est = input("Urbanización: ")

    colegio_anterior = input("Colegio anterior: ")

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

    nombre = input("Nombre completo: ")

    # >>> CAMBIO: antes era input("DNI: ")
    dni = pedir_dni()

    direccion = input("Dirección: ")

    urbanizacion = input("Urbanización: ")

    # >>> CAMBIO: antes era input("Teléfono: ")
    telefono = pedir_telefono("Teléfono: ")

    correo = input("Correo: ")

    trabajo = input("Centro de trabajo: ")

    cargo = input("Cargo: ")

    telefono_trabajo = input("Teléfono del trabajo: ")

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

    # Convertimos la opción ingresada a entero
    opcion = int(input("Seleccione una opción: "))

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
            # Mostramos los datos del estudiante
            mostrar_estudiante(estudiante)

            # Mostramos los datos del padre
            mostrar_adulto("DATOS DEL PADRE", padre)

            # Mostramos los datos de la madre
            mostrar_adulto("DATOS DE LA MADRE", madre)

            # Mostramos los datos del apoderado
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
