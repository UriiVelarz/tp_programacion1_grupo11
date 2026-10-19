import re

import Usuarios


usuarios = [
    {"id": 1, "nombre": "Admin", "contrasena": "", "rol": "administrador"},
    {"id": 2, "nombre": "FacundoGozio", "contrasena": "", "rol": "cliente"},
    {"id": 3, "nombre": "TomasGallo", "contrasena": "", "rol": "cliente"},
    {"id": 4, "nombre": "AgustinT", "contrasena": "", "rol": "cliente"},
    {"id": 5, "nombre": "Uri_Velardez", "contrasena": "", "rol": "cliente"}

]
ROLES = {"administrador", "cliente"}
MAX_INTENTOS = 3
PROXIMO_ID_USUARIO = 1


def normalizar_usuario(nombre):
    if nombre is None:
        return ""
    nombre = nombre.strip().replace("_", " ")
    nombre = " ".join(nombre.split())
    return nombre.title()


def nombre_valido(nombre):
    if nombre is None:
        return False
    nombre = normalizar_usuario(nombre)
    if nombre == "":
        return False
    return nombre.isalpha()


def contrasena_valida(contrasena):
    return re.fullmatch(r"[^\W\d_]+", contrasena, re.UNICODE) is not None


def siguiente_id_usuario():
    global PROXIMO_ID_USUARIO
    ids_registrados = {int(usuario["id"]) for usuario in usuarios}
    ids_registrados.update(int(id_usuario) for id_usuario in Usuarios.usuarios)

    while PROXIMO_ID_USUARIO in ids_registrados:
        PROXIMO_ID_USUARIO += 1

    id_usuario = f"{PROXIMO_ID_USUARIO:05d}"
    PROXIMO_ID_USUARIO += 1
    return id_usuario


def buscar_usuario(nombre, contrasena):
    nombre_normalizado = normalizar_usuario(nombre)
    for usuario in usuarios:
        if (
            normalizar_usuario(usuario["nombre"]) == nombre_normalizado
            and usuario["contrasena"] == contrasena
        ):
            return usuario
    return None


def registrar_usuario():
    while True:
        nombre = input("Nuevo nombre de usuario o -1 para volver al menu principal: ").strip()
        if nombre == "-1":
            print("Volviendo al menu principal...")
            return None

        nombre = normalizar_usuario(nombre)
        if not nombre_valido(nombre):
            print("El nombre debe contener solo letras, sin numeros, espacios ni caracteres especiales. Ejemplo: Facundo.")
            continue

        while True:
            contrasena = input("Ingrese una contraseña (solo letras) o -1 para volver: ").strip()
            if contrasena == "-1":
                print("Volviendo al menu principal...")
                return None
            if not contrasena_valida(contrasena):
                print("La contraseña debe contener solo letras, sin numeros ni caracteres especiales.")
                continue
            if any(
                normalizar_usuario(usuario["nombre"]) == normalizar_usuario(nombre)
                and usuario["contrasena"] == contrasena
                for usuario in usuarios
            ):
                print("Ya existe una cuenta con ese usuario y contraseña. Elija otra contraseña.")
                continue
            break

        datos_personales = Usuarios.solicitar_datos_personales()
        if datos_personales is None:
            return None

        nuevo = {
            "id": siguiente_id_usuario(),
            "nombre": nombre,
            "contrasena": contrasena,
            "rol": "cliente"
        }
        usuarios.append(nuevo)
        Usuarios.usuarios[int(nuevo["id"])] = {
            "nombre": nombre,
            **datos_personales
        }
        print(f"Usuario {nombre} registrado correctamente. Su ID es {nuevo['id']}.")
        return nuevo


   
def iniciar_sesion():
    while True:
        nombre = input("Usuario o -1 para volver al menu principal: ").strip()
        if nombre == "-1":
            print("Volviendo al menu principal...")
            return None

        nombre = normalizar_usuario(nombre)
        contrasena = input("Contraseña: ")
        usuario = buscar_usuario(nombre, contrasena)
        if usuario is not None:
            if usuario["rol"] not in ROLES:
                print("El usuario tiene un rol invalido.")
                return None
            print(f"Bienvenido/a, {usuario['nombre']} ({usuario['rol']})")
            return usuario

        print("Usuario o contraseña incorrectos. Intente nuevamente.")