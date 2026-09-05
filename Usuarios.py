def imprimir_Usuarios(matriz):
    print("="*60)
    print(f"{"Usuarios":42}")
    print("="*60)
    print(f"{"Id":<10}{"Nombre":<12}{"Edad":<8}{"Mail":<25}{"Telefono":<12}")
    print("-" *60)

    for i in range (len(matriz)):
        id       = matriz [i][0]
        nombre   = matriz [i][1]
        edad     = matriz [i][2]
        mail     = matriz [i][3]
        telefono = matriz [i][4]
        print(f"{id:<10}{nombre:<12}{edad:<8}{mail:<25}{telefono:<12}")

def registrar_Usuario(matriz):
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

def eliminar_Usuario(matriz):
    id = int(input("Ingresar Id: "))
    i = 0
    while i < len(matriz):
        if matriz [i][0] == id:
            matriz.remove(matriz[i])
            print("Usuario eliminado correctamente")
            return
        i = i+1
    print("No se encontro el id de usuario")

usuarios = [
    [1234, "Juan",  18, "juan@gmail.com",  11553834],
    [8254, "Agus",  12, "agus@gmail.com",  11512294],
    [4567, "Maria", 25, "maria@gmail.com", 11456789],
    [2130, "pablo", 22, "pablo@gmail.com", 11654321],
    [1101, "Pedro", 69, "pedro@gmail.com", 11452991],
    [3653, "facu",  27, "facu@gmail.com",  11635381],
    [9999, "sofi",  11, "sofi@gmail.com",  11421199]
]

#imprimir_Usuarios(usuarios)
#registrar_Usuario(usuarios)
#imprimir_Usuarios(usuarios)
#eliminar_Usuario(usuarios)
#imprimir_Usuarios(usuarios)

ordenado_Id   = sorted(usuarios, key=lambda fila: fila[0])               
ordenado_Edad = sorted(usuarios, key=lambda fila: fila[2])
#imprimir_Usuarios(ordenado_Id)

mayores = list(filter(lambda usuarios: usuarios[2] >= 18, usuarios))
#imprimir_Usuarios(mayores)

def modificar_Usuario(matriz):
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

if __name__ == "__main__":
    imprimir_Usuarios(usuarios)
    modificar_Usuario(usuarios)
    imprimir_Usuarios(usuarios)


#imprimir_Usuarios(usuarios)
#modificar_Usuario(usuarios)
#imprimir_Usuarios(usuarios)