import re

usuarios = {
    1: {"nombre": "Admin", "edad": None, "mail": "", "telefono": "", "contrasena": "", "rol": "administrador"},
    2: {"nombre": "Facundo", "edad": 27, "mail": "facu@hotmail.com", "telefono": "+54 9 1159993061", "contrasena": "", "rol": "cliente"},
    3: {"nombre": "Tomas", "edad": 21, "mail": "tomi@hotmail.com", "telefono": "+54 9 1158682965", "contrasena": "", "rol": "cliente"},
    4: {"nombre": "Agustin", "edad": 20, "mail": "agus@hotmail.com", "telefono": "+54 9 1154683065", "contrasena": "", "rol": "cliente"},
    5: {"nombre": "Uriel", "edad": 19, "mail": "uri@hotmail.com", "telefono": "+54 9 1154183061", "contrasena": "", "rol": "cliente"},
}

ROLES = {"administrador", "cliente"}
MAX_INTENTOS = 3

def volver_al_menu(valor):
    if valor == "-1":
        print("Volviendo al menu principal...")
        return True
    return False


def normalizar_usuario(nombre):
    if nombre is None:
        return ""
    nombre = nombre.strip().replace("_", " ")
    return " ".join(nombre.split()).title()


def nombre_valido(nombre):
    nombre = normalizar_usuario(nombre)
    return bool(nombre) and nombre.replace(" ", "").isalpha()


def contrasena_valida(contrasena):
    return re.fullmatch(r"[^\W\d_]+", contrasena, re.UNICODE) is not None


def mail_valido(mail):
    return re.fullmatch(
        r"[^@\s]+@(gmail\.com|hotmail\.com|yahoo\.com|outlook\.com)",
        mail,
        re.IGNORECASE
    ) is not None


def siguiente_id_usuario():
    id_usuario = 1
    while id_usuario in usuarios:
        id_usuario += 1
    return id_usuario


def solicitar_datos_personales():
    while True:
        edad_input = input("Ingresar edad (entre 18 y 95)  (-1 para volver): ").strip()
        if volver_al_menu(edad_input):
            return None
        try:
            edad = int(edad_input)
        except ValueError:
            print("La edad debe ser un numero entero entre 18 y 95.")
            continue
        if 18 <= edad <= 95:
            break
        print("La edad debe estar entre 18 y 95.")

    while True:
        mail = input("Ingresar mail (gmail.com, hotmail.com, yahoo.com u outlook.com)  (-1 para volver): ").strip()
        if volver_al_menu(mail):
            return None
        if mail_valido(mail):
            break
        print("El mail debe finalizar con @gmail.com, @hotmail.com, @yahoo.com o @outlook.com.")

    while True:
        telefono = input("Ingresar los 8 digitos del telefono  (-1 para volver): ").strip()
        if volver_al_menu(telefono):
            return None
        if re.fullmatch(r"[0-9]{8}", telefono):
            break
        print("El telefono debe contener exactamente 8 digitos numericos.")

    return {
        "edad": edad,
        "mail": mail,
        "telefono": f"+54 9 11 {telefono}",
    }


def imprimir_Usuarios(usuarios):
    print("=" * 105)
    print(f"{'Usuarios':55}")
    print("=" * 105)
    print(f"{'Id':<8}{'Nombre':<20}{'Edad':<8}{'Mail':<30}{'Telefono':<23}{'Rol':<16}")
    print("-" * 105)

    for id_usuario, usuario in sorted(
        usuarios.items(), key=lambda item: (item[1].get("nombre") or "").lower()
    ):
        edad = usuario.get("edad")
        edad = "" if edad is None else edad
        print(
            f"{str(id_usuario):<8}{usuario.get('nombre', ''):<20}"
            f"{str(edad):<8}{usuario.get('mail', '')[:28]:<30}"
            f"{usuario.get('telefono', ''):<23}{usuario.get('rol', 'cliente'):<16}"
        )


def registrar_Usuario(usuarios):
    id_input = input("Ingresar ID  (-1 para volver): ").strip()
    if volver_al_menu(id_input):
        return
    try:
        id_usuario = int(id_input)
    except ValueError:
        print("El ID debe ser un numero entero.")
        return
    if id_usuario in usuarios:
        print("ID ya registrado.")
        return

    nombre = input("Ingresar nombre  (-1 para volver): ").strip()
    if volver_al_menu(nombre):
        return
    datos = solicitar_datos_personales()
    if datos is None:
        return

    contrasena = input("Ingresar contrasena (solo letras; puede dejarse vacia para configurarla despues): ").strip()
    if contrasena and not contrasena_valida(contrasena):
        print("La contrasena debe contener solo letras.")
        return

    usuarios[id_usuario] = {
        "nombre": nombre,
        **datos,
        "contrasena": contrasena,
        "rol": "cliente",
    }
    print("Usuario registrado correctamente.")


def eliminar_Usuario(usuarios):
    id_input = input("Ingresar ID  (-1 para volver): ").strip()
    if volver_al_menu(id_input):
        return
    try:
        id_usuario = int(id_input)
    except ValueError:
        print("El ID debe ser un numero entero.")
        return
    if id_usuario in usuarios:
        del usuarios[id_usuario]
        print("Usuario eliminado correctamente.")
    else:
        print("No se encontro el ID de usuario.")


def modificar_Usuario(usuarios):
    id_input = input("Ingresar ID del usuario a modificar  (-1 para volver): ").strip()
    if volver_al_menu(id_input):
        return
    try:
        id_usuario = int(id_input)
    except ValueError:
        print("El ID debe ser un numero entero.")
        return
    if id_usuario not in usuarios:
        print("Usuario no encontrado.")
        return

    usuario = usuarios[id_usuario]
    nombre = input("Ingresar nuevo nombre  (-1 para volver): ").strip()
    if volver_al_menu(nombre):
        return
    usuario["nombre"] = nombre

    while True:
        edad_input = input("Ingresar nueva edad (18-95)  (-1 para volver): ").strip()
        if volver_al_menu(edad_input):
            return
        try:
            edad = int(edad_input)
        except ValueError:
            print("La edad debe ser un numero entero.")
            continue
        if 18 <= edad <= 95:
            usuario["edad"] = edad
            break
        print("La edad debe estar entre 18 y 95.")

    while True:
        mail = input("Ingresar nuevo mail  (-1 para volver): ").strip()
        if volver_al_menu(mail):
            return
        if mail_valido(mail):
            usuario["mail"] = mail
            break
        print("El mail no es valido.")

    telefono = input("Ingresar los 8 digitos del nuevo telefono  (-1 para volver): ").strip()
    if volver_al_menu(telefono):
        return
    if not re.fullmatch(r"[0-9]{8}", telefono):
        print("El telefono debe contener exactamente 8 digitos numericos.")
        return
    usuario["telefono"] = f"+54 9 11 {telefono}"
    print("Usuario modificado correctamente.")


def buscar_usuario(nombre, contrasena):
    nombre_normalizado = normalizar_usuario(nombre)
    for id_usuario, usuario in usuarios.items():
        if (
            normalizar_usuario(usuario.get("nombre")) == nombre_normalizado
            and usuario.get("contrasena", "") == contrasena
        ):
            # Se incluye el ID en la informacion devuelta para poder usarlo
            # en otras partes del programa.
            return {"id": id_usuario, **usuario}
    return None


def registrar_usuario():
    """Registro desde login: crea la cuenta en el mismo diccionario del CRUD."""
    while True:
        nombre = input("Nuevo nombre de usuario  (-1 para volver): ").strip()
        if volver_al_menu(nombre):
            return None
        nombre = normalizar_usuario(nombre)
        if not nombre_valido(nombre):
            print("El nombre debe contener solo letras y espacios.")
            continue
        if any(normalizar_usuario(u.get("nombre")) == nombre for u in usuarios.values()):
            print("Ese nombre de usuario ya existe. Elija otro.")
            continue
        break

    while True:
        contrasena = input("Ingrese una contrasena (solo letras)  (-1 para volver): ").strip()
        if volver_al_menu(contrasena):
            return None
        if contrasena_valida(contrasena):
            break
        print("La contrasena debe contener solo letras, sin numeros ni caracteres especiales.")

    datos_personales = solicitar_datos_personales()
    if datos_personales is None:
        return None

    id_usuario = siguiente_id_usuario()
    nuevo = {
        "nombre": nombre,
        **datos_personales,
        "contrasena": contrasena,
        "rol": "cliente",
    }
    usuarios[id_usuario] = nuevo
    print(f"Usuario {nombre} registrado correctamente. Su ID es {id_usuario}.")
    return {"id": id_usuario, **nuevo}


def iniciar_sesion():
    intentos = 0
    while intentos < MAX_INTENTOS:
        nombre = input("Usuario  (-1 para volver): ").strip()
        if volver_al_menu(nombre):
            return None
        contrasena = input("Contrasena: ")
        usuario = buscar_usuario(nombre, contrasena)
        if usuario is not None:
            if usuario.get("rol") not in ROLES:
                print("El usuario tiene un rol invalido.")
                return None
            if not usuario.get("contrasena"):
                print("Esta cuenta todavia no tiene contrasena configurada. Contacte al administrador o registre una contrasena desde su gestion de usuarios.")
                return None
            print(f"Bienvenido/a, {usuario['nombre']} ({usuario['rol']})")
            return usuario
        intentos += 1
        print(f"Usuario o contrasena incorrectos. Intentos restantes: {MAX_INTENTOS - intentos}")
    print("Se alcanzo el maximo de intentos.")
    return None