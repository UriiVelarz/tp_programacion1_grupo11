usuarios = {
    1234: {"nombre": "Juan", "edad": 18, "mail": "juan@gmail.com", "telefono": 11553834},
    8254: {"nombre": "Agus", "edad": 12, "mail": "agus@gmail.com", "telefono": 11512294},
    4567: {"nombre": "Maria", "edad": 25, "mail": "maria@gmail.com", "telefono": 11456789},
    2130: {"nombre": "pablo", "edad": 22, "mail": "pablo@gmail.com", "telefono": 11654321},
    1101: {"nombre": "Pedro", "edad": 69, "mail": "pedroherrera@gmail.com", "telefono": 11452991},
    3653: {"nombre": "facu", "edad": 27, "mail": "facundogozio@gmail.com", "telefono": 11635381},
    9999: {"nombre": "sofi", "edad": 11, "mail": "sofi@gmail.com", "telefono": 11421199}
}


def volver_al_menu(valor):
    if valor == "-1":
        print("Volviendo al menu principal...")
        return True
    return False


def imprimir_Usuarios(usuarios):
    '''
    pre: recibe un diccionario de usuarios, donde cada clave es el id
         y cada valor es otro diccionario con los datos del usuario.
    pos: devuelve por pantalla los usuarios formateados.
    '''
    print("=" * 65)
    print(f"{'Usuarios':42}")
    print("=" * 65)
    print(f"{'Id':<10}{'Nombre':<12}{'Edad':<8}{'Mail':<25}{'Telefono':<12}")
    print("-" * 65)

    for id_usuario, usuario in usuarios.items():
        mail = usuario['mail']
        if len(mail) > 20:
            mail = mail[:20] + "..."
        print(f"{id_usuario:<10}{usuario['nombre']:<12}{usuario['edad']:<8}{mail:<25}{usuario['telefono']:<12}")


def registrar_Usuario(usuarios):
    '''
        pre: recibe un diccionario de usuarios.
        pos: solicita los datos para registrar a un nuevo usuario. si el id ya existe,
             muestra error y finaliza. si el id es unico,
             agrega un usuario al diccionario y muestra un mensaje de exito.
    '''

    id_usuario_input = input("Ingresar Id o -1 para volver al menu principal: ")
    if volver_al_menu(id_usuario_input):
        return
    id_usuario = int(id_usuario_input)

    if id_usuario in usuarios:
        print("Id ya registrado")
        return

    nombre = input("Ingresar Nombre o -1 para volver al menu principal: ")
    if volver_al_menu(nombre):
        return

    edad_input = input("Ingresar Edad o -1 para volver al menu principal: ")
    if volver_al_menu(edad_input):
        return
    edad = int(edad_input)

    mail = input("Ingresar Mail o -1 para volver al menu principal: ")
    if volver_al_menu(mail):
        return

    telefono_input = input("Ingresar Telefono o -1 para volver al menu principal: ")
    if volver_al_menu(telefono_input):
        return
    telefono = int(telefono_input)

    usuarios[id_usuario] = {
        "nombre": nombre,
        "edad": edad,
        "mail": mail,
        "telefono": telefono
    }

    print("Usuario registrado correctamente")


def eliminar_Usuario(usuarios):
    '''
    pre: recibe un diccionario de usuarios.
    pos: solicita un id por consola. si el id existe en el diccionario,
         elimina al usuario y muestra un mensaje de exito.
         si no existe, muestra un mensaje de error.
    '''

    id_usuario_input = input("Ingresar Id o -1 para volver al menu principal: ")
    if volver_al_menu(id_usuario_input):
        return
    id_usuario = int(id_usuario_input)

    if id_usuario in usuarios:
        del usuarios[id_usuario]
        print("Usuario eliminado correctamente")
        return

    print("No se encontro el id de usuario")


def modificar_Usuario(usuarios):
    '''
        pre: recibe un diccionario de usuarios.
        pos: solicita un id por consola. si existe, solicita los datos a modificar
             (nombre, edad, mail, telefono) para reemplazar los valores originales
             del usuario y muestra un mensaje de exito.
    '''

    id_buscado_input = input("Ingresar id del usuario a modificar o -1 para volver al menu principal: ")
    if volver_al_menu(id_buscado_input):
        return
    id_buscado = int(id_buscado_input)

    if id_buscado not in usuarios:
        print("Usuario no encontrado")
        return

    usuario = usuarios[id_buscado]

    nombre = input("Ingresar nuevo nombre o -1 para volver al menu principal: ")
    if volver_al_menu(nombre):
        return
    usuario["nombre"] = nombre

    edad_input = input("Ingresar nueva edad o -1 para volver al menu principal: ")
    if volver_al_menu(edad_input):
        return
    usuario["edad"] = int(edad_input)

    mail = input("Ingresar nuevo mail o -1 para volver al menu principal: ")
    if volver_al_menu(mail):
        return
    usuario["mail"] = mail

    telefono_input = input("Ingresar nuevo telefono o -1 para volver al menu principal: ")
    if volver_al_menu(telefono_input):
        return
    usuario["telefono"] = int(telefono_input)

    print("Usuario modificado correctamente")
