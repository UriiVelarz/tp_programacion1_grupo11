# Sistema de disponibilidad de salas usando matriz
# Fila = sala
# Columna = día

salas = ["Sala 1", "Sala 2", "Sala 3"]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# 1 = disponible, 0 = ocupado
matriz_disponibilidad = [
    [1, 1, 0, 1, 1, 0, 1],  # Sala 1
    [0, 1, 1, 1, 0, 1, 1],  # Sala 2
    [1, 0, 1, 0, 1, 1, 1],  # Sala 3
]


def mostrar_matriz():
    print("\nMatriz de disponibilidad por sala y día")
    print("\t" + "\t".join(dias))

    for i in range(len(salas)):
        fila = [str(matriz_disponibilidad[i][j]) for j in range(len(dias))]
        print(f"{salas[i]}:\t" + "\t".join(fila))

    print("\nLeyenda: 1 = disponible, 0 = ocupado")


def consultar_disponibilidad(sala, dia):
    if sala < 1 or sala > len(salas):
        return "La sala ingresada no existe."
    if dia < 1 or dia > len(dias):
        return "El día ingresado no existe."

    disponible = matriz_disponibilidad[sala - 1][dia - 1]

    if disponible == 1:
        return f"La {salas[sala - 1]} está disponible el día {dias[dia - 1]}."
    return f"La {salas[sala - 1]} NO está disponible el día {dias[dia - 1]}."


# Menú principal
while True:
    print("\n=== RESERVA DE SALAS ===")
    print("1. Ver matriz de disponibilidad")
    print("2. Consultar día disponible por coordenadas")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        mostrar_matriz()

    elif opcion == "2":
        try:
            sala = int(input("Ingrese la sala (1 a 3): "))
            dia = int(input("Ingrese el día (1 a 7): "))
            print(consultar_disponibilidad(sala, dia))
        except ValueError:
            print("Debe ingresar valores numéricos.")

    elif opcion == "3":
        print("Gracias que tenga un buen día.")
        break

    else:
        print("Opción inválida.")

