'''
Teste do genero DB
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.genero_db import (
    get_generos,
    get_genero_by_id,
    get_genero_by_nome,
    insert_genero,
    update_genero,
    delete_genero,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_get_generos(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_genero.py::test_get_generos -vv
    '''
    try:
        generos = get_generos(db_conection)
        assert generos
        assert isinstance(generos, list)
        assert len(generos) == 3
        for indice, genero in enumerate(generos):
            assert genero
            assert isinstance(genero, dict)
            assert 'id' in genero
            assert 'nome' in genero
            assert genero['id'] == indice + 1
            assert genero['nome'] == f'genero{indice + 1}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_get_genero_by_id_inexistente(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_genero.py::test_get_genero_by_id_inexistente -vv
    '''
    identificacao = 999
    try:
        genero = get_genero_by_id(db_conection, identificacao)
        assert not genero
        assert isinstance(genero, dict)
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('identificacao', [1,2,3])
def test_get_genero_by_id(db_conection: Cursor, identificacao: int):
    '''
    Teste carga
    pytest tests/db/test_genero.py::test_get_genero_by_id -vv
    '''
    try:
        genero = get_genero_by_id(db_conection, identificacao)
        assert genero
        assert isinstance(genero, dict)
        assert 'id' in genero
        assert 'nome' in genero
        assert genero['id'] == identificacao
        assert genero['nome'] == f'genero{identificacao}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('nome', ['genero1','genero2','genero3'])
def test_get_genero_by_nome(db_conection: Cursor, nome: str):
    '''
    Teste carga
    pytest tests/db/test_genero.py::test_get_genero_by_nome -vv
    '''
    try:
        genero = get_genero_by_nome(db_conection, nome)
        assert genero
        assert isinstance(genero, dict)
        assert 'id' in genero
        assert 'nome' in genero
        assert genero['nome'] == nome
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_criar_genero_voltaire(db_conection: Cursor):
    '''
    Teste criar genero
    pytest tests/db/test_genero.py::test_criar_genero_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        insert_genero(db_conection, voltaire)
        genero = get_genero_by_nome(db_conection, voltaire)
        assert genero
        assert genero['nome'] == voltaire
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_alterar_genero_voltaire(db_conection: Cursor):
    '''
    Teste alterar genero voltaire
    pytest tests/db/test_genero.py::test_alterar_genero_voltaire -vv
    '''
    voltaire = 'voltaire'
    nome_alterado = voltaire + ' ALTERADO'
    try:
        genero = get_genero_by_nome(db_conection, voltaire)
        assert genero
        identificacao: int = genero['id']
        update_genero(db_conection, nome_alterado, identificacao)
        genero = get_genero_by_id(db_conection, identificacao)
        assert genero
        assert genero['nome'] == nome_alterado
        # Voltando com o nome original
        update_genero(db_conection, voltaire, identificacao)
        genero = get_genero_by_nome(db_conection, voltaire)
        assert genero
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_genero_voltaire(db_conection: Cursor):
    '''
    Teste excluir genero voltaire
    pytest tests/db/test_genero.py::test_excluir_genero_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        genero = get_genero_by_nome(db_conection, voltaire)
        assert genero
        identificacao: int = genero['id']
        delete_genero(db_conection, identificacao)
        genero = get_genero_by_id(db_conection, identificacao)
        assert not genero
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
