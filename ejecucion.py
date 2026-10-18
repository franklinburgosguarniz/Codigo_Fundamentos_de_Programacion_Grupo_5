# ============================================================
#  COLEGIO MARIANO MELGAR - SISTEMA DE REGISTRO DIGITAL
# ============================================================
import registro_matricula as matricula
import registro_materiales as materiales
import registro_inasistencias as inasistencias


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
    while opcion != 6:
        print("\n===== REGISTRO DE MATRÍCULA =====")
        print("1. Registrar matrícula")
        print("2. Buscar matrícula por código")
        print("3. Mostrar todas las matrículas")
        print("4. Ordenar por nombre")
        print("5. Confirmar matrícula")
        print("6. Volver")
        opcion = pedir_opcion(6)

        if opcion == 1:
            matricula.registrar_matricula()
        elif opcion == 2:
            i = matricula.buscar_matricula(input("Código (ej. MAT-0001): "))
            if i == -1:
                print("No se encontró la matrícula.")
            else:
                matricula.mostrar_matricula(i)
        elif opcion == 3:
            matricula.mostrar_matriculas()
        elif opcion == 4:
            matricula.ordenar_por_nombre()
        elif opcion == 5:
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
            docente = input("Nombre del docente: ")
            print("Total entregado:", materiales.total_por_docente(docente))


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
            estudiante = input("Nombre del estudiante: ")
            total, justificadas = inasistencias.contar_inasistencias(estudiante)
            print("Total de inasistencias:", total, "| Justificadas:", justificadas)


# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------
def menu_principal():
    opcion = 0
    while opcion != 4:
        print("\n======================================")
        print("       COLEGIO MARIANO MELGAR")
        print("     SISTEMA DE REGISTRO DIGITAL")
        print("======================================")
        print("1. Registro de matrícula")
        print("2. Registro de materiales")
        print("3. Registro de inasistencias")
        print("4. Salir")
        opcion = pedir_opcion(4)

        if opcion == 1:
            menu_matricula()
        elif opcion == 2:
            menu_materiales()
        elif opcion == 3:
            menu_inasistencias()
    print("Gracias por utilizar el sistema.")


# ------------------------------------------------------------
# EJECUCIÓN DEL PROGRAMA
# ------------------------------------------------------------
def ejecucion():
    # Se leen los archivos para recuperar los registros guardados
    matricula.cargar_archivo()
    materiales.cargar_archivo()
    inasistencias.cargar_archivo()
    menu_principal()


ejecucion()