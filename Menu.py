import Reservas
import Usuarios

def menu_principal():
    usuarios = []
    reservas = []

    while True:
        print ("\n=== Sistema de reserva de salas ===")
        print ("1. Registrarse")
        print ("2. Iniciar sesion")
        print ("3. Realizar reserva")
        print ("4. Ver reservas")
        print ("5. cerrar sesion")
        print ("0. Salir")
        opcion = input ()

        if opcion == "1":
            Usuarios.registrar_Usuario(usuarios)

        elif opcion == "3":
            Reservas.realizar_Reserva(reservas)

        elif opcion == "4":
            Reservas.imprimir_Reservas(reservas)

        elif opcion == "0":
            print("Saliendo del sistema")
            break

        else:
            print("Opcion invalida, intenta otra vez.")

#menu_principal()