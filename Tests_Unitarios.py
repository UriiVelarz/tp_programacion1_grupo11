from Usuarios import (volver_al_menu, normalizar_usuario, nombre_valido, contrasena_valida, mail_valido)

def test_volver_al_menu():
    assert volver_al_menu("-1") == True
    assert volver_al_menu("1")  == False


def test_normalizar_usuario():
    assert normalizar_usuario("  Juan  Perez  ") == "Juan Perez"
    assert normalizar_usuario("Maria")           == "Maria"
    assert normalizar_usuario(None)              == ""


def test_nombre_valido():
    assert nombre_valido("Juan") == True
    assert nombre_valido("   ")  == False
    assert nombre_valido("")     == False


def test_contrasena_valida():
    assert contrasena_valida("Maria")   == True
    assert contrasena_valida("12345")   == False
    assert contrasena_valida("Juan123") == False
    assert contrasena_valida("Juan@")   == False


def test_mail_valido():
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