import datetime
import os
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from Usuarios import (volver_al_menu, normalizar_usuario, nombre_valido, contrasena_valida, mail_valido)
import Usuarios
import Salas
import Reservas

def test_volver_al_menu():
    '''
    pre: utiliza la funcion volver_al_menu() para realizar pruebas con distintos
         valores de entrada.
    pos: verifica que devuelva True cuando recibe "-1" y False cuando recibe
         cualquier otro valor, comprobando su correcto funcionamiento.
    '''
    assert volver_al_menu("-1") == True
    assert volver_al_menu("1")  == False


def test_normalizar_usuario():
    '''
    pre: utiliza la funcion normalizar_usuario() para probar distintos nombres,
         incluyendo nombres con espacios repetidos y un valor None.
    pos: verifica que los nombres se normalicen correctamente, eliminando los
         espacios innecesarios y devolviendo una cadena vacia cuando recibe None.
    '''
    assert normalizar_usuario("  Juan  Perez  ") == "Juan Perez"
    assert normalizar_usuario("Maria")           == "Maria"
    assert normalizar_usuario(None)              == ""


def test_nombre_valido():
    '''
    pre: utiliza la funcion nombre_valido() para probar nombres con contenido,
         cadenas vacias y cadenas compuestas solamente por espacios.
    pos: verifica que acepte nombres con contenido y rechace aquellos que,
         luego de normalizarse, quedan vacios.
    '''
    assert nombre_valido("Juan") == True
    assert nombre_valido("   ")  == False
    assert nombre_valido("")     == False


def test_contrasena_valida():
    '''
    pre: utiliza la funcion contrasena_valida() para probar contrasenas
         compuestas por letras, numeros y caracteres especiales.
    pos: verifica que acepte contrasenas formadas unicamente por letras
         y rechace aquellas que contienen numeros o caracteres especiales.
    '''
    assert contrasena_valida("Maria")   == True
    assert contrasena_valida("12345")   == False
    assert contrasena_valida("Juan123") == False
    assert contrasena_valida("Juan@")   == False


def test_mail_valido():
    '''
    pre: utiliza la funcion mail_valido() para probar direcciones de correo
         electronico con distintos dominios permitidos y formatos incorrectos.
    pos: verifica que acepte direcciones pertenecientes a gmail.com, hotmail.com,
         yahoo.com y outlook.com, y rechace aquellas que no cumplen con el
         formato o los dominios establecidos.
    '''
    assert mail_valido("usuario@gmail.com")   == True
    assert mail_valido("usuario@hotmail.com") == True
    assert mail_valido("usuario@yahoo.com")   == True
    assert mail_valido("usuario@outlook.com") == True
    assert mail_valido("usuario@gmail")       == False
    assert mail_valido("usuariogmail.com")    == False


def test_configuracion_de_tipos_sala():
    assert Salas.TIPOS_SALA
    assert all(
        datos["capacidad_minima"] <= datos["capacidad_maxima"]
        for datos in Salas.TIPOS_SALA.values()
    )


def test_inicio_sesion_reintenta_sin_pedir_usuario_otra_vez():
    usuarios_originales = Usuarios.usuarios
    Usuarios.usuarios = {
        1: {
            "nombre": "Ana",
            "edad": 25,
            "mail": "ana@gmail.com",
            "telefono": "",
            "contrasena": "correcta",
            "rol": "cliente",
        }
    }
    entradas = ["Inexistente", "Ana", "incorrecta", "correcta"]
    salida = StringIO()
    try:
        with patch("builtins.input", side_effect=entradas) as entrada, redirect_stdout(salida):
            usuario = Usuarios.iniciar_sesion()
        assert usuario["nombre"] == "Ana"
        assert entrada.call_count == 4
        assert entrada.call_args_list[0].args[0].startswith("Usuario")
        assert entrada.call_args_list[1].args[0].startswith("Usuario")
        assert entrada.call_args_list[2].args[0].startswith("Contrasena")
        assert entrada.call_args_list[3].args[0].startswith("Contrasena")
        assert "Usuario no existente." in salida.getvalue()
        assert "Contrasena incorrecta." in salida.getvalue()
    finally:
        Usuarios.usuarios = usuarios_originales


def test_salas_agregadas_y_eliminadas_se_persisten():
    salas_originales = Salas.salas
    archivo_original = Salas.ARCHIVO_SALAS
    temporal_original = Salas.ARCHIVO_TEMPORAL_SALAS
    persistencia_original = Salas._persistencia_salas_habilitada
    try:
        with tempfile.TemporaryDirectory() as directorio:
            Salas.ARCHIVO_SALAS = os.path.join(directorio, "salas.txt")
            Salas.ARCHIVO_TEMPORAL_SALAS = Salas.ARCHIVO_SALAS + ".tmp"
            Salas._persistencia_salas_habilitada = True
            Salas.salas = [[10, "Sala pequeña A", 2, 1]]
            Salas._guardar_salas(Salas.salas)

            Salas.salas.clear()
            Salas._cargar_salas()
            assert len(Salas.salas) == 1
            assert Salas.salas[0][0] == 10

            Salas.salas.clear()
            Salas._guardar_salas(Salas.salas)
            Salas._cargar_salas()
            assert Salas.salas == []
    finally:
        Salas.salas = salas_originales
        Salas.ARCHIVO_SALAS = archivo_original
        Salas.ARCHIVO_TEMPORAL_SALAS = temporal_original
        Salas._persistencia_salas_habilitada = persistencia_original
        Salas.actualizar_cantidad_tipos()


def test_reservas_finalizadas_se_eliminan_y_persisten():
    reservas_originales = Reservas.reservas
    archivo_original = Reservas.ARCHIVO_RESERVAS
    temporal_original = Reservas.ARCHIVO_TEMPORAL_RESERVAS
    persistencia_original = Reservas._persistencia_habilitada
    try:
        with tempfile.TemporaryDirectory() as directorio:
            Reservas.ARCHIVO_RESERVAS = os.path.join(directorio, "reservas.txt")
            Reservas.ARCHIVO_TEMPORAL_RESERVAS = (
                Reservas.ARCHIVO_RESERVAS + ".tmp"
            )
            Reservas._persistencia_habilitada = True
            Reservas.reservas = [
                [1, 1, 1, "04/11/2026", "09:00", "11:00"],
                [2, 1, 1, "01/01/9999", "18:00", "20:00"],
            ]
            Reservas._guardar_reservas(Reservas.reservas)

            Reservas.limpiar_reservas_vencidas(
                datetime.datetime(2026, 11, 4, 12, 0)
            )
            assert [reserva[0] for reserva in Reservas.reservas] == [2]

            Reservas.reservas.clear()
            Reservas._cargar_reservas()
            assert [reserva[0] for reserva in Reservas.reservas] == [2]
    finally:
        Reservas.reservas = reservas_originales
        Reservas.ARCHIVO_RESERVAS = archivo_original
        Reservas.ARCHIVO_TEMPORAL_RESERVAS = temporal_original
        Reservas._persistencia_habilitada = persistencia_original


if __name__ == "__main__":
    tests = [test_volver_al_menu, test_normalizar_usuario, test_nombre_valido, test_contrasena_valida, test_mail_valido, test_configuracion_de_tipos_sala, test_inicio_sesion_reintenta_sin_pedir_usuario_otra_vez, test_salas_agregadas_y_eliminadas_se_persisten, test_reservas_finalizadas_se_eliminan_y_persisten]

    fallidos = 0
    for test in tests:
        try:
            test()
            print(f"Ok  {test.__name__}")
        except AssertionError:
            fallidos += 1
            print(f"FALLO {test.__name__}")
    print(f"\n{len(tests) - fallidos} pasaron, {fallidos} fallaron")