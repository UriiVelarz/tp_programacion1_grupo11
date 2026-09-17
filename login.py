credenciales = [
    ["admin", "admin123", "administrador"],
    ["facundogozio", "facundo2026", "administrador"],
    ["tomasgallo", "tomas2026", "administrador"],
    ["agustintantardini", "agustin2026", "administrador"],
    ["urielvelardez", "uriel2026", "administrador"],
]
MAX_INTENTOS = 3


def buscar_usuario(nombre):
    for i in credenciales:
        if i[0].lower() == nombre:
            return i
    return None


def clave_valida(clave):
    letras = "abcdefghijklmnopqrstuvwxyz"
    numeros = "0123456789"
    tiene_letra = False
    tiene_numero = False
    for c in clave:
        if c.lower() in letras:
            tiene_letra = True
        elif c in numeros:
            tiene_numero = True
    return len(clave) >= 6 and tiene_letra and tiene_numero


def registrar_usuario():
    nombre = input("Nuevo nombre de usuario o -1 para volver al menu principal: ").lower()
    if nombre == "-1":
        print("Volviendo al menu principal...")
        return None
    if nombre == "" or buscar_usuario(nombre) is not None:
        print("Nombre vacio o ya registrado.")
        return None
    clave = input("Clave (min. 6 caracteres, letras y numeros) o -1 para volver al menu principal: ")
    if clave == "-1":
        print("Volviendo al menu principal...")
        return None
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
        nombre = input("Usuario o -1 para volver al menu principal: ").lower()
        if nombre == "-1":
            print("Volviendo al menu principal...")
            return None
        clave = input("Clave o -1 para volver al menu principal: ")
        if clave == "-1":
            print("Volviendo al menu principal...")
            return None
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
        print("1. Iniciar sesion")
        print("2. Registrarse")
        print("3. Salir")
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