usuarios = [
    [1234, "Juan",  18, "juan@gmail.com",  11553834],
    [8254, "Agus",  12, "agus@gmail.com",  11512294],
    [4567, "Maria", 25, "maria@gmail.com", 11456789],
    [2130, "pablo", 22, "pablo@gmail.com", 11654321],
    [1101, "Pedro", 69, "pedro@gmail.com", 11452991],
    [3653, "facu",  27, "facu@gmail.com",  11635381],
    [9999, "sofi",  11, "sofi@gmail.com",  11421199]
]

def imprimir_Usuarios(matriz):
    ''' 
    pre: recibe una matriz de usuarios, donde cada fila representa un usuario con sus datos [id, nombre, edad, mail, telefono].
    pos: devuelve por pantalla la matriz de usuarios fomateada.
    ''' 
    print("="*65)
    print(f"{"Usuarios":42}")
    print("="*65)
    print(f"{"Id":<10}{"Nombre":<12}{"Edad":<8}{"Mail":<25}{"Telefono":<12}")
    print("-" *65)

    for i in range (len(matriz)):
        id       = matriz [i][0]
        nombre   = matriz [i][1]
        edad     = matriz [i][2]
        mail     = matriz [i][3]
        telefono = matriz [i][4]
        print(f"{id:<10}{nombre:<12}{edad:<8}{mail:<25}{telefono:<12}")

def registrar_Usuario(matriz):
    ''' 
        pre: recibe una matriz de usuarios, donde cada fila representa un usuario con sus datos [id, nombre, edad, mail, telefono].
        pos: solicita los datos para registrar a un nuevo usuario. si el id ya existe, muestra error y finaliza. si el id es unico, 
             agrega un usuario a la matriz al final de la lista y muestra un mensaje de exito.
    ''' 

    id       = int(input("Ingresar Id: "))
    # verifico si el id esta en la matriz
    for usuario in matriz:
        if usuario[0] == id:
            print("Id ya registrado")
            return
    nombre   = input("Ingresar Nombre: ")
    edad     = int(input("Ingresar Edad: "))
    mail     = input("Ingresar Mail: ")
    telefono = int(input("Ingresar Telefono: "))

    nuevoUsuario = [id, nombre, edad, mail, telefono]

    matriz.append(nuevoUsuario)
    print("Usuario registrado correctamente")

def eliminar_Usuario(matriz):
    ''' 
    pre: recibe una matriz de usuarios, donde cada fila representa un usuario con sus datos [id, nombre, edad, mail, telefono].
    pos: solicita un id por consola. si el id existe en la matriz, elimina al usuario de la matriz original y muestra un mensaje de exito.
         si no existe, muestra un mensaje de error.
    ''' 

    id = int(input("Ingresar Id: "))
    i = 0
    while i < len(matriz):
        if matriz [i][0] == id:
            matriz.remove(matriz[i])
            print("Usuario eliminado correctamente")
            return
        i = i+1
    print("No se encontro el id de usuario")

def modificar_Usuario(matriz):
    ''' 
        pre: recibe una matriz de usuarios, donde cada fila representa un usuario con sus datos [id, nombre, edad, mail, telefono].
        pos: solicita un id por consola hasta encontrar uno valido en la matriz. una vez encontrado, solicita los datos a modificar
             (nombre, edad, mail, telefono) para reemplazar a los valores originales del usuario y muestra un mensaje de exito.
    ''' 

    usuario_encontrado = False

    while not usuario_encontrado:
        id_buscado = int(input("Ingresar id del usuario a modificar: "))

        for fila in matriz:
            if fila[0] == id_buscado:
                usuario_encontrado = True
                fila[1] = input("Ingresar nuevo nombre: ")
                fila[2] = int(input("Ingresar nueva edad: "))
                fila[3] = input("Ingresar nuevo mail: ")
                fila[4] = int(input("Ingresar nuevo telefono: "))
                print("Usuario modificado correctamente")

        if not usuario_encontrado:
            print("Usuario no encontrado. Intente nuevamente.")
