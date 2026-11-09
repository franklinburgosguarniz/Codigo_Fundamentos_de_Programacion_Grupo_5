# ============================================================
#  COLEGIO MARIANO MELGAR - INICIO DE SESIÓN (LOGIN)
# ============================================================
import os
import hashlib

ARCHIVO = "usuarios.txt"
MAX_INTENTOS = 3

# Arreglos paralelos: la posición i de cada lista pertenece al mismo usuario
usuarios = []
nombres = []
claves = []      # se guarda la clave encriptada, nunca en texto plano
roles = []

ROLES = ("Directora", "Profesor", "Secretaria")

# Módulos del sistema a los que puede entrar cada rol (se pueden cambiar aquí)
PERMISOS = {
    "Directora":  ["Registro de matrícula", "Registro de materiales", "Registro de inasistencias"],
    "Secretaria": ["Registro de matrícula", "Registro de materiales"],
    "Profesor":   ["Registro de materiales", "Registro de inasistencias"],
}


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def validar_texto(texto):
    """Devuelve True si el texto no está vacío y no usa el separador '|'."""
    return texto != "" and "|" not in texto


def validar_usuario(usuario):
    """Mínimo 4 caracteres, sin espacios y sin '|'."""
    return len(usuario) >= 4 and " " not in usuario and "|" not in usuario


def validar_clave(clave):
    """Mínimo 4 caracteres y sin '|'."""
    return len(clave) >= 4 and "|" not in clave


def validar_rol(opcion):
    return opcion.isdigit() and 1 <= int(opcion) <= len(ROLES)


def pedir_dato(mensaje, validar, error):
    """Repite la pregunta hasta que el dato sea válido y lo devuelve limpio."""
    dato = input(mensaje).strip()
    while not validar(dato):
        print("  Error:", error)
        dato = input(mensaje).strip()
    return dato


# ------------------------------------------------------------
# SEGURIDAD
# ------------------------------------------------------------
def encriptar(clave):
    """Convierte la clave en un código (SHA-256) para no guardarla en texto plano."""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


# ------------------------------------------------------------
# CONSULTA
# ------------------------------------------------------------
def buscar_usuario(usuario):
    """Búsqueda secuencial por nombre de usuario. Devuelve la posición o -1."""
    usuario = usuario.strip().lower()
    for i in range(len(usuarios)):
        if usuarios[i] == usuario:
            return i
    return -1


def modulos_permitidos(rol):
    """Devuelve la lista de módulos que puede usar el rol."""
    return PERMISOS[rol]


def mostrar_usuarios():
    print("\n--- USUARIOS DEL SISTEMA ---")
    for i in range(len(usuarios)):
        print("Usuario :", usuarios[i])
        print("Nombre  :", nombres[i])
        print("Rol     :", roles[i])
        print("-" * 40)


# ------------------------------------------------------------
# INICIO DE SESIÓN
# ------------------------------------------------------------
def iniciar_sesion():
    """Pide usuario y clave (máximo 3 intentos).
    Devuelve la posición del usuario o -1 si se bloquea o escribe 'salir'."""
    print("\n======================================")
    print("       COLEGIO MARIANO MELGAR")
    print("          INICIO DE SESIÓN")
    print("======================================")
    print("(Escriba 'salir' como usuario para cerrar el programa)")

    intentos = 0
    while intentos < MAX_INTENTOS:
        usuario = input("Usuario: ").strip().lower()
        if usuario == "salir":
            return -1
        clave = input("Contraseña: ").strip()

        i = buscar_usuario(usuario)
        if i != -1 and claves[i] == encriptar(clave):
            print("\nBienvenido(a)", nombres[i], "- Rol:", roles[i])
            return i

        intentos = intentos + 1
        restantes = MAX_INTENTOS - intentos
        if restantes > 0:
            print("  Usuario o contraseña incorrectos. Intentos restantes:", restantes)

    print("  Demasiados intentos fallidos. Acceso bloqueado.")
    return -1


# ------------------------------------------------------------
# ADMINISTRACIÓN DE USUARIOS
# ------------------------------------------------------------
def registrar_usuario():
    """Crea un usuario nuevo (solo lo usa la directora)."""
    print("--- NUEVO USUARIO ---")
    nombre = pedir_dato("Nombre completo: ", validar_texto,
                        "el nombre no puede estar vacío ni contener '|'.")
    usuario = pedir_dato("Usuario (mín. 4 caracteres, sin espacios): ", validar_usuario,
                         "mínimo 4 caracteres, sin espacios ni '|'.").lower()
    if buscar_usuario(usuario) != -1:
        print("  Error: ya existe un usuario con ese nombre.")
        return
    clave = pedir_dato("Contraseña (mín. 4 caracteres): ", validar_clave,
                       "mínimo 4 caracteres y sin '|'.")
    print("Roles disponibles:")
    for k in range(len(ROLES)):
        print(" ", k + 1, "-", ROLES[k])
    opcion = pedir_dato("Rol (número): ", validar_rol, "elija un número de la lista.")

    usuarios.append(usuario)
    nombres.append(" ".join(nombre.split()).title())
    claves.append(encriptar(clave))
    roles.append(ROLES[int(opcion) - 1])
    guardar_archivo()
    print("Usuario", usuario, "creado como", roles[-1])


def cambiar_clave(i):
    """Permite al usuario que inició sesión cambiar su propia contraseña."""
    actual = input("Contraseña actual: ").strip()
    if claves[i] != encriptar(actual):
        print("  Error: la contraseña actual no es correcta.")
        return
    nueva = pedir_dato("Nueva contraseña (mín. 4 caracteres): ", validar_clave,
                       "mínimo 4 caracteres y sin '|'.")
    claves[i] = encriptar(nueva)
    guardar_archivo()
    print("Contraseña actualizada.")


def eliminar_usuario(i_actual):
    """Elimina un usuario (la directora no puede eliminarse a sí misma)."""
    usuario = input("Usuario a eliminar: ")
    i = buscar_usuario(usuario)
    if i == -1:
        print("No se encontró el usuario.")
    elif i == i_actual:
        print("  Error: no puede eliminar su propia cuenta.")
    else:
        for lista in (usuarios, nombres, claves, roles):
            lista.pop(i)
        guardar_archivo()
        print("Usuario eliminado.")


# ------------------------------------------------------------
# ARCHIVOS
# ------------------------------------------------------------
def crear_usuarios_iniciales():
    """Si no existe usuarios.txt, se crean los tres usuarios básicos."""
    iniciales = [
        ("directora",  "Directora",  "dir123",  "Directora"),
        ("secretaria", "Secretaria", "sec123",  "Secretaria"),
        ("profesor",   "Profesor",   "prof123", "Profesor"),
    ]
    for usuario, nombre, clave, rol in iniciales:
        usuarios.append(usuario)
        nombres.append(nombre)
        claves.append(encriptar(clave))
        roles.append(rol)
    guardar_archivo()


def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(usuarios)):
            campos = [usuarios[i], nombres[i], claves[i], roles[i]]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        crear_usuarios_iniciales()
        return
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            campos = linea.strip().split("|")
            if len(campos) == 4 and campos[3] in ROLES:
                usuarios.append(campos[0])
                nombres.append(campos[1])
                claves.append(campos[2])
                roles.append(campos[3])
    if len(usuarios) == 0:       # archivo vacío o dañado
        crear_usuarios_iniciales()
