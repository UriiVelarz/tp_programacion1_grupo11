import json
import os
import re

usuarios = {}

_ultimo_id_asignado = 0
ARCHIVO_USUARIOS = os.path.join(os.path.dirname(__file__), "usuarios.json")
ARCHIVO_TEMPORAL_USUARIOS = ARCHIVO_USUARIOS + ".tmp"
_persistencia_habilitada = True


def _guardar_usuarios(matriz_usuarios):
    '''
    pre: recibe un diccionario de usuarios, donde cada clave representa el ID del usuario
         y cada valor contiene sus datos [nombre, edad, mail, telefono, contrasena, rol].
    pos: guarda los usuarios y el ultimo ID asignado en el archivo usuarios.json,
         ordenando los registros por ID y utilizando un archivo temporal para evitar
         la perdida de datos ante errores durante la escritura.
    '''
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
    '''
    pre: utiliza el archivo usuarios.json, que contiene los datos de los usuarios
         registrados y el ultimo ID asignado.
    pos: lee y valida los datos del archivo, carga los usuarios en el diccionario
         correspondiente y actualiza el ultimo ID asignado. Si encuentra errores
         en el archivo, deshabilita la persistencia e informa el problema.
    '''
    global _persistencia_habilitada, _ultimo_id_asignado

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as arch:
            datos_archivo = json.load(arch)
    except FileNotFoundError:
        return
    except json.JSONDecodeError as error:
        _persistencia_habilitada = False
        print(f"Error en el archivo de usuarios: {error}")
        return
    except (OSError, UnicodeError) as error:
        _persistencia_habilitada = False
        print(f"No se pudo leer el archivo de usuarios: {error}")
        return

    if not isinstance(datos_archivo, dict):
        _persistencia_habilitada = False
        print("El archivo de usuarios no contiene un objeto JSON valido.")
        return

    usuarios_cargados = {}
    ultimo_id = _ultimo_id_asignado
    for id_texto, datos in datos_archivo.items():
        if id_texto == "_ultimo_id_asignado":
            if type(datos) is not int or datos < 0:
                _persistencia_habilitada = False
                print("El ultimo ID guardado en usuarios.json no es valido.")
                return
            ultimo_id = max(ultimo_id, datos)
            continue

        try:
            id_usuario = int(id_texto)
        except ValueError:
            _persistencia_habilitada = False
            print(f"ID invalido en el archivo de usuarios: {id_texto}.")
            return
        if not isinstance(datos, dict):
            _persistencia_habilitada = False
            print(f"Datos invalidos para el usuario {id_texto}.")
            return
        if not all(
            isinstance(datos.get(campo, ""), str)
            for campo in ("nombre", "mail", "telefono", "rol")
        ):
            _persistencia_habilitada = False
            print(f"Datos invalidos para el usuario {id_texto}.")
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
            print(f"Edad invalida para el usuario {id_texto}.")
            return
        if not isinstance(usuario["contrasena"], str):
            _persistencia_habilitada = False
            print(f"Contrasena invalida para el usuario {id_texto}.")
            return
        usuarios_cargados[id_usuario] = usuario

    usuarios.clear()
    usuarios.update(usuarios_cargados)
    _ultimo_id_asignado = max(
        ultimo_id,
        max(usuarios_cargados, default=0),
    )


ROLES = {"administrador", "cliente"}
MAX_INTENTOS = 3

def volver_al_menu(valor):
    '''
    pre: recibe un valor ingresado por el usuario.
    pos: verifica si el valor ingresado es "-1" para indicar que desea volver
         al menu principal. Devuelve True si desea regresar y False en caso contrario.
    '''
    if valor == "-1":
        print("Volviendo al menu principal...")
        return True
    return False


def normalizar_usuario(nombre):
    '''
    pre: recibe un nombre de usuario como cadena de texto.
    pos: elimina los espacios al principio y al final, reemplaza los espacios
         repetidos por uno solo y devuelve el nombre normalizado. Si recibe None,
         devuelve una cadena vacia.
    '''
    if nombre is None:
        return ""
    return " ".join(nombre.strip().split())


def nombre_valido(nombre):
    '''
    pre: recibe un nombre de usuario como cadena de texto.
    pos: elimina los espacios al principio y al final, reemplaza los espacios
         repetidos por uno solo y devuelve el nombre normalizado. Si recibe None,
         devuelve una cadena vacia.
    '''
    return bool(normalizar_usuario(nombre))


def contrasena_valida(contrasena):
    '''
    pre: recibe una contrasena ingresada por el usuario.
    pos: verifica que la contrasena contenga unicamente letras, sin numeros,
         espacios ni caracteres especiales. Devuelve True si es valida y
         False en caso contrario.
    '''
    return re.fullmatch(r"[^\W\d_]+", contrasena, re.UNICODE) is not None


def mail_valido(mail):
    '''
    pre: recibe una direccion de correo electronico ingresada por el usuario.
    pos: verifica que tenga un formato valido y que pertenezca a alguno de los
         dominios permitidos: gmail.com, hotmail.com, yahoo.com u outlook.com.
         Devuelve True si cumple las condiciones y False en caso contrario.
    '''
    return re.fullmatch(
        r"[^@\s]+@(gmail\.com|hotmail\.com|yahoo\.com|outlook\.com)",
        mail,
        re.IGNORECASE
    ) is not None


def siguiente_id_usuario(matriz_usuarios=None):
    '''
    pre: recibe opcionalmente un diccionario de usuarios, donde cada clave
         representa el ID de un usuario registrado.
    pos: genera y devuelve un nuevo ID correlativo, tomando como referencia
         el ultimo ID asignado y el mayor ID existente en el diccionario.
         Actualiza el ultimo ID asignado.
    '''
    global _ultimo_id_asignado
    matriz_usuarios = usuarios if matriz_usuarios is None else matriz_usuarios
    _ultimo_id_asignado = max(
        _ultimo_id_asignado,
        max(matriz_usuarios, default=0),
    ) + 1
    return _ultimo_id_asignado


def _usuario_repetido(nombre, matriz_usuarios, excluir_id=None):
    '''
    pre: recibe un nombre de usuario, un diccionario de usuarios registrados
         y opcionalmente un ID que debe excluirse de la comparacion.
    pos: verifica si el nombre ingresado ya pertenece a otro usuario, ignorando
         diferencias entre mayusculas y minusculas y espacios innecesarios.
         Devuelve True si el nombre esta repetido y False en caso contrario.
    '''
    nombres_registrados = {
        normalizar_usuario(usuario.get("nombre")).casefold()
        for id_usuario, usuario in matriz_usuarios.items()
        if id_usuario != excluir_id
    }
    return normalizar_usuario(nombre).casefold() in nombres_registrados


def solicitar_datos_personales():
    '''
    pre: no recibe parametros.
    pos: solicita la edad, el mail y el telefono del usuario, validando que la
         edad este entre 18 y 95 años, que el mail pertenezca a un dominio
         permitido y que el telefono contenga exactamente 8 digitos. Devuelve
         un diccionario con los datos personales validados o None si el usuario
         decide volver al menu principal.
    '''
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
    '''
    pre: recibe un diccionario de usuarios, donde cada clave representa el ID
         del usuario y cada valor contiene sus datos personales y su rol.
    pos: muestra por pantalla todos los usuarios registrados, ordenados por ID,
         incluyendo su nombre, edad, mail, telefono y rol.
    '''
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
    '''
    pre: recibe un diccionario de usuarios registrados.
    pos: solicita el nombre, los datos personales y la contrasena del nuevo usuario,
         validando que el nombre no este repetido y que los datos sean correctos.
         Genera un nuevo ID, registra al usuario con rol cliente y guarda los cambios.
    '''
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

    id_usuario = siguiente_id_usuario(matriz_usuarios)
    matriz_usuarios[id_usuario] = {
        "nombre": nombre,
        **datos,
        "contrasena": contrasena,
        "rol": "cliente",
    }
    _guardar_usuarios(matriz_usuarios)
    print(f"Usuario registrado correctamente. Su ID es {id_usuario}.")


def eliminar_Usuario(usuarios):
    '''
    pre: recibe un diccionario de usuarios, donde cada clave representa el ID
         del usuario registrado.
    pos: solicita el ID del usuario que se desea eliminar, verifica que sea un
         numero entero y que exista en el diccionario. Si existe, lo elimina
         y guarda los cambios realizados.
    '''
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
    '''
    pre: recibe un diccionario de usuarios registrados.
    pos: solicita el ID del usuario que se desea modificar y permite actualizar
         su nombre, edad, mail, telefono y contrasena. Valida los nuevos datos,
         conserva los campos que no se desean modificar y guarda los cambios.
    '''
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

    usuario = usuarios[id_usuario].copy()
    while True:
        nombre = input("Ingresar nuevo nombre de usuario (Enter para mantenerlo; -1 para volver): ").strip()
        if volver_al_menu(nombre):
            return
        if not nombre:
            break
        nombre = normalizar_usuario(nombre)
        if not nombre_valido(nombre):
            print("El nombre de usuario no puede estar vacio.")
            continue
        if _usuario_repetido(nombre, usuarios, excluir_id=id_usuario):
            print("Usuario repetido, intente otra vez.")
            continue
        usuario["nombre"] = nombre
        break

    while True:
        edad_input = input("Ingresar nueva edad (18-95; Enter para mantenerla; -1 para volver): ").strip()
        if volver_al_menu(edad_input):
            return
        if not edad_input:
            break
        try:
            edad = int(edad_input)
        except ValueError:
            print("La edad debe ser un numero entero.")
            continue
        if not 18 <= edad <= 95:
            print("La edad debe estar entre 18 y 95.")
            continue
        usuario["edad"] = edad
        break

    while True:
        mail = input("Ingresar nuevo mail (Enter para mantenerlo; -1 para volver): ").strip()
        if volver_al_menu(mail):
            return
        if not mail:
            break
        if not mail_valido(mail):
            print("El mail no es valido.")
            continue
        usuario["mail"] = mail
        break

    while True:
        telefono = input("Ingresar los 8 digitos del nuevo telefono " "(Enter para mantenerlo; -1 para volver): ").strip()
        if volver_al_menu(telefono):
            return
        if not telefono:
            break
        if not re.fullmatch(r"[0-9]{8}", telefono):
            print("El telefono debe contener exactamente 8 digitos numericos.")
            continue
        usuario["telefono"] = f"+54 9 11 {telefono}"
        break

    while True:
        contrasena = input("Ingresar nueva contrasena (solo letras; Enter para mantenerla; -1 para volver): ").strip()
        if volver_al_menu(contrasena):
            return
        if not contrasena:
            break
        if not contrasena_valida(contrasena):
            print("La contrasena debe contener solo letras.")
            continue
        usuario["contrasena"] = contrasena
        break

    usuarios[id_usuario] = usuario
    _guardar_usuarios(usuarios)
    print("Usuario modificado correctamente.")


def gestionar_rol_administrador(matriz_usuarios, administrador):
    '''
    pre: recibe un diccionario de usuarios registrados y los datos del administrador
         que realiza la operacion.
    pos: verifica que quien realiza la operacion sea el administrador superior
         (ID 1). Solicita el ID de un usuario y alterna su rol entre cliente y
         administrador, impidiendo modificar el rol del administrador superior.
         Guarda los cambios realizados.
    '''
    if administrador.get("id") != 1 or administrador.get("rol") != "administrador":
        print("Solo el administrador superior puede gestionar roles de administrador.")
        return

    id_input = input("Ingresar ID del usuario al que desea asignar o quitar el rol administrador " "(-1 para volver): ").strip()
    if volver_al_menu(id_input):
        return
    try:
        id_usuario = int(id_input)
    except ValueError:
        print("El ID debe ser un numero entero.")
        return
    if id_usuario == 1:
        print("No se puede modificar el rol del administrador superior.")
        return
    if id_usuario not in matriz_usuarios:
        print("Usuario no encontrado.")
        return

    usuario = matriz_usuarios[id_usuario]
    if usuario.get("rol") == "administrador":
        usuario["rol"] = "cliente"
        print(f"El usuario {usuario['nombre']} ahora tiene rol cliente.")
    else:
        usuario["rol"] = "administrador"
        print(f"El usuario {usuario['nombre']} ahora tiene rol administrador.")
    _guardar_usuarios(matriz_usuarios)


def buscar_usuario(nombre, contrasena, posicion=0):
    '''
    pre: recibe un nombre de usuario, una contrasena y una posicion inicial
         para recorrer el diccionario global de usuarios.
    pos: busca recursivamente un usuario que coincida con el nombre y la
         contrasena ingresados. Devuelve un diccionario con sus datos e ID
         si encuentra una coincidencia, o None si no existe.
    '''
    ids = list(usuarios.keys())

    if posicion >= len(ids):
        return None

    id_usuario = ids[posicion]
    usuario = usuarios[id_usuario]

    nombre_buscado = normalizar_usuario(nombre).lower()
    nombre_usuario = normalizar_usuario(usuario["nombre"]).lower()

    if nombre_usuario == nombre_buscado and usuario["contrasena"] == contrasena:
        resultado = {"id": id_usuario}
        for clave in usuario:
            resultado[clave] = usuario[clave]
        return resultado

    return buscar_usuario(nombre, contrasena, posicion + 1)


def registrar_usuario():
    '''
    pre: utiliza el diccionario global de usuarios para registrar una nueva cuenta
         desde la pantalla de inicio de sesion.
    pos: solicita y valida el nombre, la contrasena y los datos personales del
         nuevo usuario. Genera un ID correlativo, registra la cuenta con rol
         cliente, guarda los cambios y devuelve un diccionario con los datos
         del usuario registrado y su ID.
    '''
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
    '''
    pre: utiliza el diccionario global de usuarios y la cantidad maxima de
         intentos permitidos para verificar las credenciales ingresadas.
    pos: solicita el nombre de usuario y la contrasena, verifica que coincidan
         con una cuenta registrada y que esta tenga un rol valido y una contrasena
         configurada. Devuelve los datos del usuario si inicia sesion correctamente
         o None si cancela o supera la cantidad maxima de intentos.
    '''
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