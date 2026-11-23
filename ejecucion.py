# ============================================================
#  COLEGIO MARIANO MELGAR - SISTEMA DE REGISTRO DIGITAL
# ============================================================
import registro_matricula as matricula
import registro_materiales as materiales
import registro_inasistencias as inasistencias
import login


def pedir_opcion(maximo):
    """Pide una opción del menú y repite hasta que sea un número válido."""
    opcion = input("Seleccione una opción: ").strip()
    while not (opcion.isdigit() and 1 <= int(opcion) <= maximo):
        print("  Opción incorrecta.")
        opcion = input("Seleccione una opción: ").strip()
    return int(opcion)


# ------------------------------------------------------------
# SUBMENÚ: MATRÍCULA
# ------------------------------------------------------------
def menu_matricula():
    opcion = 0
    while opcion != 8:
        print("\n===== REGISTRO DE MATRÍCULA =====")
        print("1. Registrar matrícula")
        print("2. Buscar matrícula por código")
        print("3. Buscar matrícula por DNI")
        print("4. Mostrar todas las matrículas")
        print("5. Mostrar matrículas pendientes")
        print("6. Ordenar por apellido")
        print("7. Confirmar matrícula")
        print("8. Volver")
        opcion = pedir_opcion(8)

        if opcion == 1:
            matricula.registrar_matricula()
        elif opcion == 2:
            i = matricula.buscar_matricula(input("Código (ej. MAT-0001): "))
            if i == -1:
                print("No se encontró la matrícula.")
            else:
                matricula.mostrar_matricula(i)
        elif opcion == 3:
            dni = matricula.pedir_dato("DNI (8 dígitos): ", matricula.validar_dni,
                                       "el DNI debe tener 8 dígitos numéricos.")
            i = matricula.buscar_por_dni(dni)
            if i == -1:
                print("No se encontró la matrícula.")
            else:
                matricula.mostrar_matricula(i)
        elif opcion == 4:
            matricula.mostrar_matriculas()
        elif opcion == 5:
            matricula.mostrar_pendientes()
        elif opcion == 6:
            matricula.ordenar_por_apellido()
        elif opcion == 7:
            matricula.confirmar_matricula(input("Código (ej. MAT-0001): "))


# ------------------------------------------------------------
# SUBMENÚ: MATERIALES
# ------------------------------------------------------------
def menu_materiales():
    opcion = 0
    while opcion != 5:
        print("\n===== REGISTRO DE MATERIALES =====")
        print("1. Registrar solicitud de material")
        print("2. Buscar solicitud por código")
        print("3. Mostrar todas las solicitudes")
        print("4. Total de material entregado a un docente")
        print("5. Volver")
        opcion = pedir_opcion(5)

        if opcion == 1:
            materiales.registrar_material()
        elif opcion == 2:
            i = materiales.buscar_material(input("Código (ej. MTR-0001): "))
            if i == -1:
                print("No se encontró la solicitud.")
            else:
                materiales.mostrar_material(i)
        elif opcion == 3:
            materiales.mostrar_materiales()
        elif opcion == 4:
            materiales.consultar_total_docente()


# ------------------------------------------------------------
# SUBMENÚ: INASISTENCIAS
# ------------------------------------------------------------
def menu_inasistencias():
    opcion = 0
    while opcion != 6:
        print("\n===== REGISTRO DE INASISTENCIAS =====")
        print("1. Registrar inasistencia")
        print("2. Buscar inasistencia por código")
        print("3. Mostrar todas las inasistencias")
        print("4. Ordenar por fecha")
        print("5. Contar inasistencias de un estudiante")
        print("6. Volver")
        opcion = pedir_opcion(6)

        if opcion == 1:
            inasistencias.registrar_inasistencia()
        elif opcion == 2:
            i = inasistencias.buscar_inasistencia(input("Código (ej. INA-0001): "))
            if i == -1:
                print("No se encontró la inasistencia.")
            else:
                inasistencias.mostrar_inasistencia(i)
        elif opcion == 3:
            inasistencias.mostrar_inasistencias()
        elif opcion == 4:
            inasistencias.ordenar_por_fecha()
        elif opcion == 5:
            print("Buscar al estudiante por:")
            print("1. Nombre completo")
            print("2. DNI")
            if pedir_opcion(2) == 1:
                inasistencias.consultar_por_nombre()
            else:
                inasistencias.consultar_por_dni()


# ------------------------------------------------------------
# MENÚS PRINCIPALES SEGÚN EL PERFIL
# ------------------------------------------------------------
def mostrar_encabezado(i):
    print("\n======================================")
    print("       COLEGIO MARIANO MELGAR")
    print("     SISTEMA DE REGISTRO DIGITAL")
    print("======================================")
    print("Sesión:", login.nombres[i], "-", login.roles[i])


def menu_directora(i):
    """La dirección ve todos los registros y administra los usuarios."""
    opcion = 0
    while opcion != 7:
        mostrar_encabezado(i)
        print("1. Registro de matrícula")
        print("2. Registro de materiales")
        print("3. Registro de inasistencias")
        print("4. Ver usuarios")
        print("5. Agregar usuario")
        print("6. Cambiar mi usuario y contraseña")
        print("7. Cerrar sesión")
        opcion = pedir_opcion(7)

        if opcion == 1:
            menu_matricula()
        elif opcion == 2:
            menu_materiales()
        elif opcion == 3:
            menu_inasistencias()
        elif opcion == 4:
            login.ver_usuarios()
        elif opcion == 5:
            login.agregar_usuario()
        elif opcion == 6:
            login.cambiar_credenciales(i)


def menu_secretaria(i):
    """La secretaria gestiona matrículas e inasistencias."""
    opcion = 0
    while opcion != 4:
        mostrar_encabezado(i)
        print("1. Registro de matrícula")
        print("2. Registro de inasistencias")
        print("3. Cambiar mi usuario y contraseña")
        print("4. Cerrar sesión")
        opcion = pedir_opcion(4)

        if opcion == 1:
            menu_matricula()
        elif opcion == 2:
            menu_inasistencias()
        elif opcion == 3:
            login.cambiar_credenciales(i)


def menu_profesor(i):
    """El profesor solicita materiales y registra inasistencias."""
    opcion = 0
    while opcion != 4:
        mostrar_encabezado(i)
        print("1. Registro de materiales")
        print("2. Registro de inasistencias")
        print("3. Cambiar mi usuario y contraseña")
        print("4. Cerrar sesión")
        opcion = pedir_opcion(4)

        if opcion == 1:
            menu_materiales()
        elif opcion == 2:
            menu_inasistencias()
        elif opcion == 3:
            login.cambiar_credenciales(i)


# ------------------------------------------------------------
# EJECUCIÓN DEL PROGRAMA
# ------------------------------------------------------------
def ejecucion():
    # Se leen los archivos para recuperar los registros guardados
    login.cargar_archivo()
    matricula.cargar_archivo()
    materiales.cargar_archivo()
    inasistencias.cargar_archivo()

    # El menú de acceso se repite hasta que se elija "Terminar el programa"
    i = login.iniciar_sesion()
    while i != -1:
        perfil = login.perfil_de_rol(login.roles[i])
        if perfil == 1:
            menu_directora(i)
        elif perfil == 2:
            menu_secretaria(i)
        else:
            menu_profesor(i)
        print("Sesión cerrada.")
        i = login.iniciar_sesion()
    print("Gracias por utilizar el sistema.")


ejecucion()
