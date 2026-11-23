# ============================================================
#  COLEGIO MARIANO MELGAR - INICIO DE SESIÓN Y USUARIOS
# ============================================================
import os
import sys
import hashlib
from getpass import getpass
import registro_matricula as matricula   # se reutiliza la validación de nombre completo

ARCHIVO = "usuarios.txt"
MAX_INTENTOS = 3
LETRAS_USUARIO = "abcdefghijklmnopqrstuvwxyz0123456789"
DIGITOS_HEXA = "0123456789abcdef"

# Roles que puede tener un usuario y perfiles del menú de acceso
ROLES = ["Directora", "Director", "Secretaria", "Profesor", "Profesora"]
PERFILES = ["Director(a)", "Secretaria", "Profesor(a)"]

# Arreglos paralelos: la posición i de cada lista pertenece al mismo usuario
nombres = []
usuarios = []
claves = []      # guarda el hash de cada contraseña, nunca la contraseña real
roles = []


# ------------------------------------------------------------
# PROTECCIÓN DE CONTRASEÑAS
# ------------------------------------------------------------
def generar_hash(clave):
    """Convierte una contraseña en su hash SHA-256 (64 caracteres hexadecimales).
    El hash no se puede revertir: solo se compara con el de lo que se escribe al ingresar."""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def es_hash(texto):
    """True si el texto ya tiene la forma de un hash SHA-256."""
    if len(texto) != 64:
        return False
    for caracter in texto:
        if caracter not in DIGITOS_HEXA:
            return False
    return True


# ------------------------------------------------------------
# VALIDACIONES
# ------------------------------------------------------------
def perfil_de_rol(rol):
    """Devuelve 1 (director/a), 2 (secretaria) o 3 (profesor/a) según el rol."""
    if rol == "Directora" or rol == "Director":
        return 1
    if rol == "Secretaria":
        return 2
    return 3


def buscar_usuario(usuario):
    """Devuelve la posición del nombre de usuario o -1."""
    for i in range(len(usuarios)):
        if usuarios[i] == usuario.lower():
            return i
    return -1


def validar_usuario_nuevo(usuario):
    """De 4 a 15 caracteres (letras sin tilde o números) y que no esté en uso."""
    usuario = usuario.lower()
    if not 4 <= len(usuario) <= 15:
        return False
    for caracter in usuario:
        if caracter not in LETRAS_USUARIO:
            return False
    return buscar_usuario(usuario) == -1


def validar_clave(clave):
    """Mínimo 6 caracteres, sin espacios ni el separador '|'."""
    return len(clave) >= 6 and " " not in clave and "|" not in clave


# ------------------------------------------------------------
# ENTRADA DE DATOS
# ------------------------------------------------------------
def pedir_clave(mensaje):
    """Pide una contraseña mostrando asteriscos (*) al escribir.
    Si la consola no permite ocultarla (por ejemplo algunos editores), se escribe visible."""
    if not sys.stdin.isatty():
        return input(mensaje)
    try:
        import msvcrt                      # consola de Windows
    except ImportError:
        return getpass(mensaje)            # Linux / Mac: se oculta sin asteriscos
    print(mensaje, end="", flush=True)
    clave = ""
    tecla = msvcrt.getwch()
    while tecla != "\r" and tecla != "\n":
        if tecla == "\x03":                # Ctrl+C
            raise KeyboardInterrupt
        if tecla == "\b":                  # borrar el último carácter
            if clave != "":
                clave = clave[:-1]
                print("\b \b", end="", flush=True)
        elif tecla == "\x00" or tecla == "\xe0":
            msvcrt.getwch()                # tecla especial (flechas, F1...): se ignora
        else:
            clave = clave + tecla
            print("*", end="", flush=True)
        tecla = msvcrt.getwch()
    print()
    return clave


def pedir_numero(mensaje, maximo):
    """Pide una opción numérica entre 1 y maximo."""
    opcion = input(mensaje).strip()
    while not (opcion.isdigit() and 1 <= int(opcion) <= maximo):
        print("  Opción incorrecta.")
        opcion = input(mensaje).strip()
    return int(opcion)


# ------------------------------------------------------------
# INICIO DE SESIÓN
# ------------------------------------------------------------
def pedir_credenciales(perfil):
    """Pide usuario y contraseña (3 intentos) para el perfil elegido.
    Devuelve la posición del usuario o -1 si se agotan los intentos."""
    print("\n--- Ingreso como", PERFILES[perfil - 1], "---")
    intentos = 0
    while intentos < MAX_INTENTOS:
        usuario = input("Usuario: ").strip()
        clave = pedir_clave("Contraseña: ")
        i = buscar_usuario(usuario)
        if usuario != "" and clave != "" and i != -1 and claves[i] == generar_hash(clave) and perfil_de_rol(roles[i]) == perfil:
            print("Bienvenido/a,", nombres[i])
            return i
        # Cualquier fallo (incluidos campos vacíos) cuenta como intento
        intentos = intentos + 1
        if usuario == "" or clave == "":
            print("  Error: debe ingresar su usuario y su contraseña. Intentos restantes:", MAX_INTENTOS - intentos)
        else:
            print("  Usuario o contraseña incorrectos para este perfil. Intentos restantes:",
                  MAX_INTENTOS - intentos)
    print("Acceso bloqueado: superó el máximo de intentos.")
    return -1


def iniciar_sesion():
    """Muestra el menú de acceso. Devuelve la posición del usuario que ingresó
    o -1 si se elige terminar el programa."""
    while True:
        print("\n======================================")
        print("       COLEGIO MARIANO MELGAR")
        print("          INICIO DE SESIÓN")
        print("======================================")
        print("Ingresar como:")
        print("1. Director(a)")
        print("2. Secretaria")
        print("3. Profesor(a)")
        print("4. Terminar el programa")
        opcion = pedir_numero("Seleccione una opción: ", 4)
        if opcion == 4:
            return -1
        i = pedir_credenciales(opcion)
        if i != -1:
            return i


# ------------------------------------------------------------
# GESTIÓN DE USUARIOS (solo la dirección)
# ------------------------------------------------------------
def mostrar_usuario(i):
    print("Nombre  :", nombres[i])
    print("Usuario :", usuarios[i])
    print("Rol     :", roles[i])
    print("-" * 40)


def ver_usuarios():
    """Muestra los usuarios agrupados por perfil (sin contraseñas)."""
    for perfil in (1, 2, 3):
        print("\n=== " + PERFILES[perfil - 1].upper() + " ===")
        cantidad = 0
        for i in range(len(usuarios)):
            if perfil_de_rol(roles[i]) == perfil:
                mostrar_usuario(i)
                cantidad = cantidad + 1
        if cantidad == 0:
            print("No hay usuarios registrados.")


def pedir_rol():
    print("Rol del nuevo usuario:")
    for i in range(len(ROLES)):
        print(str(i + 1) + ".", ROLES[i])
    return ROLES[pedir_numero("Seleccione el rol: ", len(ROLES)) - 1]


def pedir_clave_nueva(permitir_vacia=False):
    """Pide la contraseña dos veces para evitar errores al escribirla.
    Si permitir_vacia es True, Enter sin escribir nada devuelve '' (conservar la actual)."""
    while True:
        clave = pedir_clave("Contraseña (mínimo 6 caracteres, sin espacios): ")
        if permitir_vacia and clave == "":
            return ""
        if not validar_clave(clave):
            print("  Error: la contraseña debe tener al menos 6 caracteres, sin espacios ni '|'.")
        elif clave != pedir_clave("Repita la contraseña: "):
            print("  Error: las contraseñas no coinciden.")
        else:
            return clave


def agregar_usuario():
    """La dirección registra un nuevo director/a, secretaria o profesor/a."""
    print("--- NUEVO USUARIO ---")
    nombre = matricula.pedir_dato("Nombre completo (nombres y apellidos): ",
                                  matricula.validar_nombre_completo,
                                  matricula.MENSAJE_NOMBRE)
    usuario = matricula.pedir_dato("Nombre de usuario (4 a 15 letras o números): ",
                                   validar_usuario_nuevo,
                                   "use de 4 a 15 letras (sin tildes ni ñ) o números, sin espacios, "
                                   "y que no esté ya en uso.")
    rol = pedir_rol()
    clave = pedir_clave_nueva()

    nombres.append(matricula.normalizar_nombre(nombre))
    usuarios.append(usuario.lower())
    claves.append(generar_hash(clave))
    roles.append(rol)
    guardar_archivo()
    print("Usuario", usuario.lower(), "registrado como", rol + ".")


def cambiar_credenciales(i):
    """Permite al usuario en sesión (posición i) cambiar su usuario y/o contraseña.
    Antes pide la contraseña actual."""
    print("--- CAMBIAR USUARIO Y CONTRASEÑA ---")
    intentos = 0
    actual = pedir_clave("Contraseña actual: ")
    while generar_hash(actual) != claves[i]:
        intentos = intentos + 1
        if intentos == MAX_INTENTOS:
            print("Contraseña incorrecta. No se realizaron cambios.")
            return
        print("  Error: la contraseña actual no es correcta. Intentos restantes:", MAX_INTENTOS - intentos)
        actual = pedir_clave("Contraseña actual: ")

    print("Deje vacío (Enter) lo que no quiera cambiar.")
    mensaje = "Nuevo nombre de usuario (actual: " + usuarios[i] + "): "
    nuevo_usuario = input(mensaje).strip().lower()
    while nuevo_usuario != "" and nuevo_usuario != usuarios[i] and not validar_usuario_nuevo(nuevo_usuario):
        print("  Error: use de 4 a 15 letras (sin tildes ni ñ) o números, sin espacios, "
              "y que no esté ya en uso.")
        nuevo_usuario = input(mensaje).strip().lower()
    print("Nueva contraseña:")
    nueva_clave = pedir_clave_nueva(True)

    if nuevo_usuario == "" and nueva_clave == "":
        print("No se realizaron cambios.")
        return
    if nuevo_usuario != "":
        usuarios[i] = nuevo_usuario
    if nueva_clave != "":
        claves[i] = generar_hash(nueva_clave)
    guardar_archivo()
    print("Datos actualizados. Su usuario ahora es:", usuarios[i])


# ------------------------------------------------------------
# ARCHIVOS
# Formato: nombre completo|usuario|hash de la contraseña|rol
# ------------------------------------------------------------
def crear_usuarios_iniciales(guardar):
    """Usuarios de ejemplo (la directora puede agregar más y cada uno puede cambiar los suyos)."""
    nombres.extend(["María Elena Quispe Rojas", "Carmen Rosa Vargas Soto", "Luis Alberto Torres Ríos"])
    usuarios.extend(["directora", "secretaria", "profesor"])
    claves.extend([generar_hash("Direc2026"), generar_hash("Secre2026"), generar_hash("Profe2026")])
    roles.extend(["Directora", "Secretaria", "Profesor"])
    if guardar:
        guardar_archivo()


def guardar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(usuarios)):
            campos = [nombres[i], usuarios[i], claves[i], roles[i]]
            archivo.write("|".join(campos) + "\n")


def cargar_archivo():
    if not os.path.exists(ARCHIVO):
        crear_usuarios_iniciales(True)      # primera ejecución: se crea el archivo
        return
    # utf-8-sig tolera el BOM que algunos editores (Bloc de notas) agregan al guardar
    convertidas = 0
    with open(ARCHIVO, "r", encoding="utf-8-sig") as archivo:
        numero = 0
        for linea in archivo:
            numero = numero + 1
            if linea.strip() == "":
                continue
            campos = linea.strip().split("|")
            valida = False
            if len(campos) == 4:
                for k in range(4):
                    campos[k] = campos[k].strip()
                rol = campos[3].capitalize()
                valida = (rol in ROLES and campos[1] != "" and campos[2] != ""
                          and buscar_usuario(campos[1]) == -1)
            if valida:
                nombres.append(campos[0])
                usuarios.append(campos[1].lower())
                if es_hash(campos[2]):
                    claves.append(campos[2])
                else:
                    # Contraseña escrita en texto (archivo antiguo o editado a mano): se convierte a hash
                    claves.append(generar_hash(campos[2]))
                    convertidas = convertidas + 1
                roles.append(rol)
            else:
                print("Aviso: se ignoró la línea", numero, "de", ARCHIVO,
                      "(formato: nombre completo|usuario|contraseña|rol, sin usuarios repetidos).")
    if convertidas > 0:
        guardar_archivo()                   # se reescribe el archivo con los hashes
    if len(usuarios) == 0:
        print("No hay usuarios válidos en", ARCHIVO + ": se usarán los usuarios iniciales.")
        crear_usuarios_iniciales(False)
