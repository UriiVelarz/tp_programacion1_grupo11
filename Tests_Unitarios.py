from Usuarios import (volver_al_menu, normalizar_usuario, nombre_valido, contrasena_valida, mail_valido)

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


if __name__ == "__main__":
    tests = [test_volver_al_menu, test_normalizar_usuario, test_nombre_valido, test_contrasena_valida, test_mail_valido]

    fallidos = 0
    for test in tests:
        try:
            test()
            print(f"Ok  {test.__name__}")
        except AssertionError:
            fallidos += 1
            print(f"FALLO {test.__name__}")
    print(f"\n{len(tests) - fallidos} pasaron, {fallidos} fallaron")