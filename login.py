usuarios = [
    ("Admin", "", "administrador"),
    ("FacundoGozio", "", "cliente"),
    ("TomasGallo", "", "cliente"),
    ("AgustinT", "", "cliente"),
    ("Uri_Velardez", "", "cliente")

]
ROLES = {"administrador", "cliente"}
MAX_INTENTOS = 3


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


def usuario_existe(nombre):
    nombres_registrados = {normalizar_usuario(usuario[0]) for usuario in usuarios}
    return normalizar_usuario(nombre) in nombres_registrados


def buscar_usuario(nombre):
    nombre_normalizado = normalizar_usuario(nombre)
    for usuario in usuarios:
        if normalizar_usuario(usuario[0]) == nombre_normalizado:
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
        if usuario_existe(nombre):
            print("Nombre ya registrado. Intente otro.")
            continue
        nuevo = (nombre, "", "cliente")
        usuarios.append(nuevo)
        print("Usuario", nombre, "registrado correctamente.")
        return nuevo


   
def iniciar_sesion():
    while True:
        nombre = input("Usuario o -1 para volver al menu principal: ").strip()
        if nombre == "-1":
            print("Volviendo al menu principal...")
            return None

        nombre = normalizar_usuario(nombre)
        usuario = buscar_usuario(nombre)
        if usuario is not None:
            nombre_usuario, _, rol = usuario
            if rol not in ROLES:
                print("El usuario tiene un rol invalido.")
                return None
            print(f"Bienvenido/a, {nombre_usuario} ({rol})")
            return usuario

        print("Usuario no encontrado. Intente nuevamente.")





