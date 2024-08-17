'''
Teste do editora DB
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.editora_db import (
    get_editoras,
    get_editora_by_id,
    get_editora_by_nome,
    insert_editora,
    update_editora,
    delete_editora,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_get_editoras(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_editora.py::test_get_editoras -vv
    '''
    try:
        editoras = get_editoras(db_conection)
        assert editoras
        assert isinstance(editoras, list)
        assert len(editoras) == 4
        for indice, editora in enumerate(editoras):
            assert editora
            assert isinstance(editora, dict)
            assert 'id' in editora
            assert 'nome' in editora
            assert editora['id'] == indice + 1
            assert editora['nome'] == f'editora{indice + 1}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_get_editora_by_id_inexistente(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_editora.py::test_get_editora_by_id_inexistente -vv
    '''
    identificacao = 999
    try:
        editora = get_editora_by_id(db_conection, identificacao)
        assert not editora
        assert isinstance(editora, dict)
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('identificacao', [1,2,3])
def test_get_editora_by_id(db_conection: Cursor, identificacao: int):
    '''
    Teste carga
    pytest tests/db/test_editora.py::test_get_editora_by_id -vv
    '''
    try:
        editora = get_editora_by_id(db_conection, identificacao)
        assert editora
        assert isinstance(editora, dict)
        assert 'id' in editora
        assert 'nome' in editora
        assert editora['id'] == identificacao
        assert editora['nome'] == f'editora{identificacao}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('nome', ['editora1','editora2','editora3'])
def test_get_editora_by_nome(db_conection: Cursor, nome: str):
    '''
    Teste carga
    pytest tests/db/test_editora.py::test_get_editora_by_nome -vv
    '''
    try:
        editora = get_editora_by_nome(db_conection, nome)
        assert editora
        assert isinstance(editora, dict)
        assert 'id' in editora
        assert 'nome' in editora
        assert editora['nome'] == nome
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_criar_editora_voltaire(db_conection: Cursor):
    '''
    Teste criar editora
    pytest tests/db/test_editora.py::test_criar_editora_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        insert_editora(db_conection, voltaire)
        editora = get_editora_by_nome(db_conection, voltaire)
        assert editora
        assert editora['nome'] == voltaire
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_alterar_editora_voltaire(db_conection: Cursor):
    '''
    Teste alterar editora voltaire
    pytest tests/db/test_editora.py::test_alterar_editora_voltaire -vv
    '''
    voltaire = 'voltaire'
    nome_alterado = voltaire + ' ALTERADO'
    try:
        editora = get_editora_by_nome(db_conection, voltaire)
        assert editora
        identificacao: int = editora['id']
        update_editora(db_conection, nome_alterado, identificacao)
        editora = get_editora_by_id(db_conection, identificacao)
        assert editora
        assert editora['nome'] == nome_alterado
        # Voltando com o nome original
        update_editora(db_conection, voltaire, identificacao)
        editora = get_editora_by_nome(db_conection, voltaire)
        assert editora
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_editora_voltaire(db_conection: Cursor):
    '''
    Teste excluir editora voltaire
    pytest tests/db/test_editora.py::test_excluir_editora_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        editora = get_editora_by_nome(db_conection, voltaire)
        assert editora
        identificacao: int = editora['id']
        delete_editora(db_conection, identificacao)
        editora = get_editora_by_id(db_conection, identificacao)
        assert not editora
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
