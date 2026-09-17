
# Columnas: [usuario, clave, rol]
credenciales = [
    ["admin", "admin123", "administrador"],
    ["facundogozio", "facundo2026", "administrador"],
    ["tomasgallo", "tomas2026", "administrador"],
    ["agustintantardini", "agustin2026", "administrador"],
    ["urielvelardez", "uriel2026", "administrador"]
]
MAX_INTENTOS = 3


def buscar_usuario(nombre):
    """Devuelve la fila del usuario si existe, o None."""
    encontrados = list(filter(lambda u: u[0] == nombre, credenciales))
    return encontrados[0] if encontrados else None


def clave_valida(clave):
    """Minimo 6 caracteres, con al menos una letra y un numero."""
    tiene_letra = tiene_numero = False
    for c in clave:
        if c.isalpha():
            tiene_letra = True
        elif c.isdigit():
            tiene_numero = True
    return len(clave) >= 6 and tiene_letra and tiene_numero


def registrar_usuario():
    nombre = input("Nuevo nombre de usuario: ").strip().lower()
    if nombre == "" or buscar_usuario(nombre) is not None:
        print("Nombre vacio o ya registrado.")
        return None
    clave = input("Clave (minimo 6 caracteres, letras y numeros): ")
    if not clave_valida(clave):
        print("La clave no cumple los requisitos.")
        return None
    nuevo = [nombre, clave, "cliente"]
    credenciales.append(nuevo)
    print("Usuario", nombre, "registrado correctamente.")
    return nuevo


def iniciar_sesion():
    intentos = 0
    while intentos < MAX_INTENTOS:
        nombre = input("Usuario: ").strip().lower()
        clave = input("Clave: ")
        u = buscar_usuario(nombre)
        if u is not None and u[1] == clave:
            print("Bienvenido/a,", nombre, "(" + u[2] + ")")
            return u
        intentos += 1
        print("Datos incorrectos. Intentos restantes:", MAX_INTENTOS - intentos)
    print("Se supero la cantidad de intentos.")
    return None


def menu_login():
    while True:
        print("\n--- ACCESO AL SISTEMA ---")
        print("1. Iniciar sesion\n2. Registrarse\n3. Salir")
        opcion = input("Opcion: ")
        if opcion == "1":
            u = iniciar_sesion()
            if u is not None:
                return u
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            return None
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    print("Sesion activa:", menu_login())
