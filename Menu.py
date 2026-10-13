import login
import Reservas
import Salas
import Usuarios
import Estadisticas

def menu_usuario_logueado(usuario):
    while True:
        print(f"\n=== Bienvenido/a {usuario['nombre']} (ID {usuario['id']}) ===")
        print("1. Reservar sala")
        print("2. Mostrar reservas")
        print("3. Modificar reserva")
        print("4. Cancelar reserva")
        print("5. Consultar disponibilidad por mes")
        print("6. Cerrar sesion")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            Reservas.realizar_Reserva(Reservas.reservas, id_usuario=usuario["id"])

        elif opcion == "2":
            Reservas.imprimir_Reservas(Reservas.reservas, usuario=usuario["id"])

        elif opcion == "3":
            Reservas.modificar_Reserva(Reservas.reservas, usuario=usuario["id"])

        elif opcion == "4":
            Reservas.eliminar_Reserva(Reservas.reservas, usuario=usuario["id"])

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
        print("4. Gestionar Salas")
        print("5. Gestionar Usuarios")
        print("6. Reportes estadisticos")
        print("7. Salir del sistema")
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
            menu_salas(Salas.salas)

        elif opcion == "5":
            menu_usuarios(Usuarios.usuarios)

        elif opcion == "6":
            Estadisticas.menu_estadisticas(Reservas.reservas, Salas.salas, Usuarios.usuarios)

        elif opcion == "7":
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion invalida, intenta otra vez.")


def menu_salas(matriz):

    while True:
        print ((f"\n=== Gestion de salas ==="))
        print("1. Alta de sala")
        print("2. listar salas")
        print("3. Modificar sala")
        print("4. Baja de sala")
        print("5. Volver")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            Salas.agregar_Sala(matriz)

        elif opcion == "2":
            Salas.imprimir_Salas(matriz)

        elif opcion == "3":
            Salas.modificar_Sala(matriz)

        elif opcion == "4":
            Salas.eliminar_Sala(matriz)

        elif opcion == "5":
            return
            
        else:
            print("Opcion invalida")

def menu_usuarios(matriz):

    while True:
        print ((f"\n=== Gestion de usuarios ==="))
        print("1. Alta de usuario")
        print("2. listar usuarios")
        print("3. Modificar usuario")
        print("4. Baja de usuario")
        print("5. Volver")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            Usuarios.registrar_Usuario(matriz)

        elif opcion == "2":
            Usuarios.imprimir_Usuarios(matriz)

        elif opcion == "3":
            Usuarios.modificar_Usuario(matriz)

        elif opcion == "4":
            Usuarios.eliminar_Usuario(matriz)

        elif opcion == "5":
            return
            
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    menu_principal()