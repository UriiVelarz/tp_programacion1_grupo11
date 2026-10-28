import json
import os
import re

usuarios = {}

_ultimo_id_asignado = 0
ARCHIVO_USUARIOS = os.path.join(os.path.dirname(__file__), "usuarios.json")
ARCHIVO_TEMPORAL_USUARIOS = ARCHIVO_USUARIOS + ".tmp"
_persistencia_habilitada = True


def _guardar_usuarios(matriz_usuarios):
    if matriz_usuarios is not usuarios:
        return
    if not _persistencia_habilitada:
        print("No se guardaron los cambios porque el archivo de usuarios no se pudo leer.")
        return

    try:
        with open(ARCHIVO_TEMPORAL_USUARIOS, "w", encoding="utf-8") as arch:
            arch.write("{\n")
            arch.write(
                json.dumps("_ultimo_id_asignado")
                + ": "
                + json.dumps(_ultimo_id_asignado)
                + (",\n" if matriz_usuarios else "\n")
            )
            usuarios_ordenados = sorted(matriz_usuarios.items())
            for indice, (id_usuario, usuario) in enumerate(usuarios_ordenados):
                registro_usuario = {
                    "nombre": usuario.get("nombre", ""),
                    "edad": usuario.get("edad"),
                    "mail": usuario.get("mail", ""),
                    "telefono": usuario.get("telefono", ""),
                    "contrasena": usuario.get("contrasena", ""),
                    "rol": usuario.get("rol", "cliente"),
                }

                arch.write(
                    json.dumps(str(id_usuario))
                    + ": "
                    + json.dumps(registro_usuario, ensure_ascii=False)
                    + ("," if indice < len(usuarios_ordenados) - 1 else "")
                    + "\n"
                )
            arch.write("}\n")
        os.replace(ARCHIVO_TEMPORAL_USUARIOS, ARCHIVO_USUARIOS)
    except (OSError, TypeError, ValueError) as error:
        try:
            os.remove(ARCHIVO_TEMPORAL_USUARIOS)
        except FileNotFoundError:
            pass
        except OSError as error_limpieza:
            print(f"No se pudo limpiar el archivo temporal: {error_limpieza}")
        print(f"No se pudieron guardar los usuarios: {error}")


def _cargar_usuarios():
    global _persistencia_habilitada, _ultimo_id_asignado

    try:
        arch = open(ARCHIVO_USUARIOS, "r", encoding="utf-8")
    except FileNotFoundError:
        return
    except (OSError, UnicodeError) as error:
        _persistencia_habilitada = False
        print(f"No se pudo leer el archivo de usuarios: {error}")
        return

    usuarios_cargados = {}
    numero_linea = 0
    try:
        with arch:
            cad = arch.readline()
            if cad.strip() != "{":
                _persistencia_habilitada = False
                print("El archivo de usuarios no contiene un objeto JSON valido.")
                return

            while True:
                cad = arch.readline()
                numero_linea += 1
                if not cad:
                    _persistencia_habilitada = False
                    print("El objeto JSON de usuarios no tiene cierre.")
                    return
                cad = cad.strip()
                if cad == "}":
                    while True:
                        cad = arch.readline()
                        if not cad:
                            break
                        if cad.strip():
                            _persistencia_habilitada = False
                            print("Hay contenido despues del objeto JSON de usuarios.")
                            return
                    break
                if not cad:
                    continue
                if cad.endswith(","):
                    cad = cad[:-1].rstrip()
                try:
                    registro = json.loads("{" + cad + "}")
                except json.JSONDecodeError as error:
                    _persistencia_habilitada = False
                    print(f"Error en la linea {numero_linea} del archivo de usuarios: {error}")
                    return

                if not isinstance(registro, dict) or len(registro) != 1:
                    _persistencia_habilitada = False
                    print(f"Formato invalido en la linea {numero_linea} del archivo de usuarios.")
                    return

                id_texto, datos = next(iter(registro.items()))
                if id_texto == "_ultimo_id_asignado":
                    if type(datos) is not int or datos < 0:
                        _persistencia_habilitada = False
                        print("El ultimo ID guardado en usuarios.json no es valido.")
                        return
                    _ultimo_id_asignado = max(_ultimo_id_asignado, datos)
                    continue
                try:
                    id_usuario = int(id_texto)
                except ValueError:
                    _persistencia_habilitada = False
                    print(f"ID invalido en la linea {numero_linea} del archivo de usuarios.")
                    return
                if not isinstance(datos, dict):
                    _persistencia_habilitada = False
                    print(f"Datos invalidos en la linea {numero_linea} del archivo de usuarios.")
                    return
                if not all(
                    isinstance(datos.get(campo, ""), str)
                    for campo in ("nombre", "mail", "telefono", "rol")
                ):
                    _persistencia_habilitada = False
                    print(f"Datos invalidos en la linea {numero_linea} del archivo de usuarios.")
                    return

                usuario = {
                    "nombre": datos.get("nombre", ""),
                    "edad": datos.get("edad"),
                    "mail": datos.get("mail", ""),
                    "telefono": datos.get("telefono", ""),
                    "contrasena": datos.get("contrasena", ""),
                    "rol": datos.get("rol", "cliente"),
                }
                if datos.get("edad") is not None and type(datos.get("edad")) is not int:
                    _persistencia_habilitada = False
                    print(f"Edad invalida en la linea {numero_linea} del archivo de usuarios.")
                    return
                if not isinstance(usuario["contrasena"], str):
                    _persistencia_habilitada = False
                    print(f"Contrasena invalida en la linea {numero_linea} del archivo de usuarios.")
                    return
                usuarios_cargados[id_usuario] = usuario
    except (OSError, UnicodeError) as error:
        _persistencia_habilitada = False
        print(f"No se pudo leer el archivo de usuarios: {error}")
        return

    usuarios.clear()
    usuarios.update(usuarios_cargados)
    _ultimo_id_asignado = max(
        _ultimo_id_asignado,
        max(usuarios_cargados, default=0),
    )


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
    return " ".join(nombre.strip().split())


def nombre_valido(nombre):
    return bool(normalizar_usuario(nombre))


def contrasena_valida(contrasena):
    return re.fullmatch(r"[^\W\d_]+", contrasena, re.UNICODE) is not None


def mail_valido(mail):
    return re.fullmatch(
        r"[^@\s]+@(gmail\.com|hotmail\.com|yahoo\.com|outlook\.com)",
        mail,
        re.IGNORECASE
    ) is not None


def siguiente_id_usuario():
    global _ultimo_id_asignado
    _ultimo_id_asignado = max(_ultimo_id_asignado, max(usuarios, default=0)) + 1
    return _ultimo_id_asignado


def _usuario_repetido(nombre, matriz_usuarios, excluir_id=None):
    nombres_registrados = {
        normalizar_usuario(usuario.get("nombre")).casefold()
        for id_usuario, usuario in matriz_usuarios.items()
        if id_usuario != excluir_id
    }
    return normalizar_usuario(nombre).casefold() in nombres_registrados


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

    for id_usuario, usuario in sorted(usuarios.items()):
        edad = usuario.get("edad")
        edad = "" if edad is None else edad
        print(
            f"{str(id_usuario):<8}{usuario.get('nombre', ''):<20}"
            f"{str(edad):<8}{usuario.get('mail', '')[:28]:<30}"
            f"{usuario.get('telefono', ''):<23}{usuario.get('rol', 'cliente'):<16}"
        )


def registrar_Usuario(matriz_usuarios):
    global _ultimo_id_asignado

    id_input = input("Ingresar ID  (-1 para volver): ").strip()
    if volver_al_menu(id_input):
        return
    try:
        id_usuario = int(id_input)
    except ValueError:
        print("El ID debe ser un numero entero.")
        return
    if id_usuario in matriz_usuarios:
        print("ID ya registrado.")
        return

    while True:
        nombre = input("Ingresar nombre de usuario  (-1 para volver): ").strip()
        if volver_al_menu(nombre):
            return
        nombre = normalizar_usuario(nombre)
        if not nombre_valido(nombre):
            print("El nombre de usuario no puede estar vacio.")
            continue
        if _usuario_repetido(nombre, matriz_usuarios):
            print("Usuario repetido, intente otra vez.")
            continue
        break

    datos = solicitar_datos_personales()
    if datos is None:
        return

    contrasena = input("Ingresar contrasena (solo letras; puede dejarse vacia para configurarla despues): ").strip()
    if contrasena and not contrasena_valida(contrasena):
        print("La contrasena debe contener solo letras.")
        return

    matriz_usuarios[id_usuario] = {
        "nombre": nombre,
        **datos,
        "contrasena": contrasena,
        "rol": "cliente",
    }
    if matriz_usuarios is usuarios:
        _ultimo_id_asignado = max(_ultimo_id_asignado, id_usuario)
    _guardar_usuarios(matriz_usuarios)
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
        _guardar_usuarios(usuarios)
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
    while True:
        nombre = input("Ingresar nuevo nombre de usuario  (-1 para volver): ").strip()
        if volver_al_menu(nombre):
            return
        nombre = normalizar_usuario(nombre)
        if not nombre_valido(nombre):
            print("El nombre de usuario no puede estar vacio.")
            continue
        if _usuario_repetido(nombre, usuarios, excluir_id=id_usuario):
            print("Usuario repetido, intente otra vez.")
            continue
        break
    usuario["nombre"] = nombre
    _guardar_usuarios(usuarios)

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
            _guardar_usuarios(usuarios)
            break
        print("La edad debe estar entre 18 y 95.")

    while True:
        mail = input("Ingresar nuevo mail  (-1 para volver): ").strip()
        if volver_al_menu(mail):
            return
        if mail_valido(mail):
            usuario["mail"] = mail
            _guardar_usuarios(usuarios)
            break
        print("El mail no es valido.")

    telefono = input("Ingresar los 8 digitos del nuevo telefono  (-1 para volver): ").strip()
    if volver_al_menu(telefono):
        return
    if not re.fullmatch(r"[0-9]{8}", telefono):
        print("El telefono debe contener exactamente 8 digitos numericos.")
        return
    usuario["telefono"] = f"+54 9 11 {telefono}"
    _guardar_usuarios(usuarios)
    print("Usuario modificado correctamente.")


def buscar_usuario(nombre, contrasena):
    nombre_normalizado = normalizar_usuario(nombre)
    for id_usuario, usuario in usuarios.items():
        if (
            normalizar_usuario(usuario.get("nombre")).casefold()
            == nombre_normalizado.casefold()
            and usuario.get("contrasena", "") == contrasena
        ):
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
            print("El nombre de usuario no puede estar vacio.")
            continue
        if _usuario_repetido(nombre, usuarios):
            print("Usuario repetido, intente otra vez.")
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
    _guardar_usuarios(usuarios)
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
            datos_guardados = usuarios.get(usuario["id"], {})
            if not datos_guardados.get("contrasena"):
                print("Esta cuenta todavia no tiene contrasena configurada. Contacte al administrador o registre una contrasena desde su gestion de usuarios.")
                return None
            print(f"Bienvenido/a, {usuario['nombre']} ({usuario['rol']})")
            return usuario
        intentos += 1
        print(f"Usuario o contrasena incorrectos. Intentos restantes: {MAX_INTENTOS - intentos}")
    print("Se alcanzo el maximo de intentos.")
    return None


_cargar_usuarios()