def imprimir_Usuarios(matriz):
    print("="*60)
    print(f"{"Usuarios":^42}")
    print("="*60)
    print(f"{"Id":<10}{"Nombre":<12}{"Edad":<8}{"Mail":<20}{"Telefono":<12}")
    print("-" *60)

    for i in range (len(matriz)):
        id       = matriz [i][0]
        nombre   = matriz [i][1]
        edad     = matriz [i][2]
        mail     = matriz [i][3]
        telefono = matriz [i][4]
        print(f"{id:<10}{nombre:<12}{edad:<8}{mail:<20}{telefono:<12}")

def agregar_Usuario(matriz):
    id       = int(input("Ingresar Id: "))
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

datos = [
    [1234, "Juan", 22, "juan@gmail.com", 11553834],
    [8254, "Agus", 32, "agus@gmail.com", 11512294],
    [4567, "Maria", 25, "maria@gmail.com", 11456789],
    [7890, "Pedro", 28, "pedro@gmail.com", 11654321],
]

imprimir_Usuarios(datos)
#agregar_Usuario(datos)
#imprimir_Usuarios(datos)
eliminar_Usuario(datos)

imprimir_Usuarios(datos)


