from Usuarios import usuarios
from Reservas import reservas

#Funciones de usuarios

#Funciones para ordenar
ordenado_Id     = sorted(usuarios, key=lambda fila: fila[0])
ordenado_Nombre = sorted(usuarios, key=lambda fila: fila[1])       
ordenado_Edad   = sorted(usuarios, key=lambda fila: fila[2])

#Funciones para filtrar
mayores = list(filter(lambda usuarios: usuarios[2] >= 18, usuarios))


#Funciones de reservas

#Funciones para ordenar
ordenFechaYHorario = sorted(reservas, key=lambda fila: (fila[3],fila[4]))

#Funciones para filtrar
id_usuario_buscado = 3653
filtrarPorId = list(filter(lambda reserva: reserva[2] == id_usuario_buscado, reservas))

#Funciones 
ids_Reservas = list(map(lambda fila: fila[0], reservas))

