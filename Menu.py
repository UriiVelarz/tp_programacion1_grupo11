import Reservas
import Salas
import Usuarios
import Estadisticas

def es_admin(usuario):
    '''
    pre: recibe un diccionario con los datos de un usuario.
    pos: devuelve True si el rol del usuario es administrador y False en caso contrario.
    '''
    return usuario.get("rol") == "administrador"

def menu_usuario_logueado(usuario):
    '''
    pre: recibe un diccionario con los datos del usuario que inicio sesion.
    pos: muestra el menu de opciones para usuarios comunes y permite realizar reservas, consultar, modificar o cancelar reservas, consultar la disponibilidad mensual y cerrar sesion.
    '''
    while True:
        Reservas.limpiar_reservas_vencidas()
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


def menu_admin(usuario):
    '''
    pre: recibe un diccionario con los datos del administrador que inicio sesion.
    pos: muestra el menu de administrador y permite gestionar salas, gestionar usuarios, consultar reportes estadisticos, consultar la disponibilidad mensual y cerrar sesion.
    '''
    while True:
        Reservas.limpiar_reservas_vencidas()
        print(f"\n=== Menu administrador: {usuario['nombre']} ===")
        print("1. Gestionar salas")
        print("2. Gestionar usuarios")
        print("3. Reportes estadisticos")
        print("4. Consultar disponibilidad por mes")
        print("5. Cerrar sesion")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            menu_salas(Salas.salas)

        elif opcion == "2":
            menu_usuarios(Usuarios.usuarios, usuario)

        elif opcion == "3":
            Estadisticas.menu_estadisticas(
                Reservas.reservas, Salas.salas, Usuarios.usuarios
            )

        elif opcion == "4":
            Salas.consultar_disponibilidad_mensual()

        elif opcion == "5":
            print("Sesion cerrada.")
            return

        else:
            print("Opcion invalida, intenta otra vez.")


def menu_principal():
    '''
    pre: utiliza los modulos de usuarios, salas, reservas y estadisticas del sistema.
    pos: muestra el menu principal y permite registrar usuarios, iniciar sesion o salir del sistema. segun el rol del usuario que inicia sesion, dirige al menu correspondiente.
    '''
    while True:
        Reservas.limpiar_reservas_vencidas()
        print("\n=== Sistema de reserva de salas ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesion")
        print("3. Salir del sistema")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            Usuarios.registrar_usuario()

        elif opcion == "2":
            usuario = Usuarios.iniciar_sesion()
            if usuario is not None:
                if es_admin(usuario):
                    menu_admin(usuario)
                else:
                    menu_usuario_logueado(usuario)

        elif opcion == "3":
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion invalida, intenta otra vez.")


def menu_salas(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila contiene los datos de una sala.
    pos: muestra el menu de gestion de salas y permite agregar, listar, modificar o eliminar salas, o volver al menu anterior.
    '''
    while True:
        Reservas.limpiar_reservas_vencidas()
        print(f"\n=== Gestion de salas ===")
        print("1. Alta de sala")
        print("2. Listar salas")
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


def menu_usuarios(matriz, administrador):
    '''
    pre: recibe una matriz de usuarios y un diccionario con los datos del administrador que realiza la gestion.
    pos: muestra el menu de gestion de usuarios y permite registrar, listar, modificar o eliminar usuarios. si el administrador tiene id 1, tambien permite asignar o quitar roles de administrador.
    '''
    while True:
        Reservas.limpiar_reservas_vencidas()
        print(f"\n=== Gestion de usuarios ===")
        print("1. Alta de usuario")
        print("2. Listar usuarios")
        print("3. Modificar usuario")
        print("4. Baja de usuario")
        if administrador.get("id") == 1:
            print("5. Asignar/quitar rol administrador")
            print("6. Volver")
        else:
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

        elif opcion == "5" and administrador.get("id") == 1:
            Usuarios.gestionar_rol_administrador(matriz, administrador)

        elif opcion == "5" and administrador.get("id") != 1:
            return

        elif opcion == "6" and administrador.get("id") == 1:
            return

        else:
            print("Opcion invalida")


if __name__ == "__main__":
    menu_principal()