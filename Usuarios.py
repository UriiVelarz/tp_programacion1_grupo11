usuarios = {
    1234: {"nombre": "Juan", "edad": 18, "mail": "juan@gmail.com", "telefono": 11553834},
    8254: {"nombre": "Agus", "edad": 12, "mail": "agus@gmail.com", "telefono": 11512294},
    4567: {"nombre": "Maria", "edad": 25, "mail": "maria@gmail.com", "telefono": 11456789},
    2130: {"nombre": "pablo", "edad": 22, "mail": "pablo@gmail.com", "telefono": 11654321},
    1101: {"nombre": "Pedro", "edad": 69, "mail": "pedroherrera@gmail.com", "telefono": 11452991},
    3653: {"nombre": "facu", "edad": 27, "mail": "facundogozio@gmail.com", "telefono": 11635381},
    9999: {"nombre": "sofi", "edad": 11, "mail": "sofi@gmail.com", "telefono": 11421199}
}


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

    id_usuario = int(input("Ingresar Id: "))

    if id_usuario in usuarios:
        print("Id ya registrado")
        return

    nombre = input("Ingresar Nombre: ")
    edad = int(input("Ingresar Edad: "))
    mail = input("Ingresar Mail: ")
    telefono = int(input("Ingresar Telefono: "))

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

    id_usuario = int(input("Ingresar Id: "))

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

    id_buscado = int(input("Ingresar id del usuario a modificar: "))

    if id_buscado not in usuarios:
        print("Usuario no encontrado")
        return

    usuario = usuarios[id_buscado]
    usuario["nombre"] = input("Ingresar nuevo nombre: ")
    usuario["edad"] = int(input("Ingresar nueva edad: "))
    usuario["mail"] = input("Ingresar nuevo mail: ")
    usuario["telefono"] = int(input("Ingresar nuevo telefono: "))

    print("Usuario modificado correctamente")
