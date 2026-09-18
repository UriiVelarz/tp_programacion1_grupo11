import login
import Reservas
import Salas


def menu_usuario_logueado(usuario):
    while True:
        print(f"\n=== Bienvenido/a {usuario[0]} ===")
        print("1. Reservar sala")
        print("2. Mostrar reservas")
        print("3. Modificar reserva")
        print("4. Cancelar reserva")
        print("5. Consultar disponibilidad por mes")
        print("6. Cerrar sesion")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            Reservas.realizar_Reserva(Reservas.reservas, id_usuario=usuario[0])

        elif opcion == "2":
            Reservas.imprimir_Reservas(Reservas.reservas, usuario=usuario[0])

        elif opcion == "3":
            Reservas.modificar_Reserva(Reservas.reservas, usuario=usuario[0])

        elif opcion == "4":
            Reservas.eliminar_Reserva(Reservas.reservas, usuario=usuario[0])

        elif opcion == "5":
            Salas.consultar_disponibilidad_mensual()

        elif opcion == "6":
            print("Sesion cerrada.")
            return

        else:
            print("Opcion invalida, intenta otra vez.")


def menu_principal():
    while True:
        print("\n=== Sistema de reserva de salas ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesion")
        print("3. Consultar disponibilidad por mes")
        print("4. Salir del sistema")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            login.registrar_usuario()

        elif opcion == "2":
            usuario = login.iniciar_sesion()
            if usuario is not None:
                menu_usuario_logueado(usuario)

        elif opcion == "3":
            Salas.consultar_disponibilidad_mensual()

        elif opcion == "4":
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion invalida, intenta otra vez.")


if __name__ == "__main__":
    menu_principal()