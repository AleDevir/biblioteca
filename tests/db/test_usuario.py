'''
Teste do usuario DB
pytest tests/db/test_usuario.py -vv
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.usuario_db import (
    get_usuarios,
    get_usuario_by_id,
    get_usuario_by_nome,
    insert_usuario,
    update_usuario,
    delete_usuario,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_get_usuarios(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_usuario.py::test_get_usuarios -vv
    '''
    try:
        usuarios = get_usuarios(db_conection)
        assert usuarios
        assert isinstance(usuarios, list)
        assert len(usuarios) == 3
        for indice, usuario in enumerate(usuarios):
            assert usuario
            assert isinstance(usuario, dict)
            assert 'id' in usuario
            assert 'nome' in usuario
            assert usuario['id'] == indice + 1
            assert usuario['nome'] == f'usuario{indice + 1}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_get_usuario_by_id_inexistente(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_usuario.py::test_get_usuario_by_id_inexistente -vv
    '''
    identificacao = 999
    try:
        usuario = get_usuario_by_id(db_conection, identificacao)
        assert not usuario
        assert isinstance(usuario, dict)
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('identificacao', [1,2,3])
def test_get_usuario_by_id(db_conection: Cursor, identificacao: int):
    '''
    Teste carga
    pytest tests/db/test_usuario.py::test_get_usuario_by_id -vv
    '''
    try:
        usuario = get_usuario_by_id(db_conection, identificacao)
        assert usuario
        assert isinstance(usuario, dict)
        assert 'id' in usuario
        assert 'nome' in usuario
        assert usuario['id'] == identificacao
        assert usuario['nome'] == f'usuario{identificacao}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('nome', ['usuario1','usuario2','usuario3'])
def test_get_usuario_by_nome(db_conection: Cursor, nome: str):
    '''
    Teste carga
    pytest tests/db/test_usuario.py::test_get_usuario_by_nome -vv
    '''
    try:
        usuario = get_usuario_by_nome(db_conection, nome)
        assert usuario
        assert isinstance(usuario, dict)
        assert 'id' in usuario
        assert 'nome' in usuario
        assert usuario['nome'] == nome
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_criar_usuario_voltaire(db_conection: Cursor):
    '''
    Teste criar usuario
    pytest tests/db/test_usuario.py::test_criar_usuario_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        insert_usuario(db_conection, voltaire, '1234567890', 'BRASIL')
        usuario = get_usuario_by_nome(db_conection, voltaire)
        assert usuario
        assert usuario['nome'] == voltaire
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_alterar_usuario_voltaire(db_conection: Cursor):
    '''
    Teste alterar usuario voltaire
    pytest tests/db/test_usuario.py::test_alterar_usuario_voltaire -vv
    '''
    voltaire = 'voltaire'
    nome_alterado = voltaire + ' ALTERADO'
    try:
        usuario = get_usuario_by_nome(db_conection, voltaire)
        assert usuario
        identificacao: int = usuario['id']
        update_usuario(db_conection, nome_alterado, '1234567890', 'BRASIL', identificacao)
        usuario = get_usuario_by_id(db_conection, identificacao)
        assert usuario
        assert usuario['nome'] == nome_alterado
        # Voltando com o nome original
        update_usuario(db_conection, voltaire, '0987654321', 'BRASIL', identificacao)
        usuario = get_usuario_by_nome(db_conection, voltaire)
        assert usuario
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_usuario_voltaire(db_conection: Cursor):
    '''
    Teste excluir usuario voltaire
    pytest tests/db/test_usuario.py::test_excluir_usuario_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        usuario = get_usuario_by_nome(db_conection, voltaire)
        assert usuario
        identificacao: int = usuario['id']
        delete_usuario(db_conection, identificacao)
        usuario = get_usuario_by_id(db_conection, identificacao)
        assert not usuario
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
