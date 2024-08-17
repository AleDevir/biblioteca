'''
Teste do Autor DB
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.autor_db import (
    get_autores,
    get_autor_by_id,
    get_autor_by_nome,
    insert_autor,
    update_autor,
    delete_autor,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_get_autores(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_autor.py::test_get_autores -vv
    '''
    try:
        autores = get_autores(db_conection)
        assert autores
        assert isinstance(autores, list)
        assert len(autores) == 3
        for indice, autor in enumerate(autores):
            assert autor
            assert isinstance(autor, dict)
            assert 'id' in autor
            assert 'nome' in autor
            assert autor['id'] == indice + 1
            assert autor['nome'] == f'autor{indice + 1}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_get_autor_by_id_inexistente(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_autor.py::test_get_autor_by_id_inexistente -vv
    '''
    identificacao = 999
    try:
        autor = get_autor_by_id(db_conection, identificacao)
        assert not autor
        assert isinstance(autor, dict)
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('identificacao', [1,2,3])
def test_get_autor_by_id(db_conection: Cursor, identificacao: int):
    '''
    Teste carga
    pytest tests/db/test_autor.py::test_get_autor_by_id -vv
    '''
    try:
        autor = get_autor_by_id(db_conection, identificacao)
        assert autor
        assert isinstance(autor, dict)
        assert 'id' in autor
        assert 'nome' in autor
        assert autor['id'] == identificacao
        assert autor['nome'] == f'autor{identificacao}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('nome', ['autor1','autor2','autor3'])
def test_get_autor_by_nome(db_conection: Cursor, nome: str):
    '''
    Teste carga
    pytest tests/db/test_autor.py::test_get_autor_by_nome -vv
    '''
    try:
        autor = get_autor_by_nome(db_conection, nome)
        assert autor
        assert isinstance(autor, dict)
        assert 'id' in autor
        assert 'nome' in autor
        assert autor['nome'] == nome
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_criar_autor_voltaire(db_conection: Cursor):
    '''
    Teste criar autor
    pytest tests/db/test_autor.py::test_criar_autor_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        insert_autor(db_conection, voltaire)
        autor = get_autor_by_nome(db_conection, voltaire)
        assert autor
        assert autor['nome'] == voltaire
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_alterar_autor_voltaire(db_conection: Cursor):
    '''
    Teste alterar autor voltaire
    pytest tests/db/test_autor.py::test_alterar_autor_voltaire -vv
    '''
    voltaire = 'voltaire'
    nome_alterado = voltaire + ' ALTERADO'
    try:
        autor = get_autor_by_nome(db_conection, voltaire)
        assert autor
        identificacao: int = autor['id']
        update_autor(db_conection, nome_alterado, identificacao)
        autor = get_autor_by_id(db_conection, identificacao)
        assert autor
        assert autor['nome'] == nome_alterado
        # Voltando com o nome original
        update_autor(db_conection, voltaire, identificacao)
        autor = get_autor_by_nome(db_conection, voltaire)
        assert autor
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_autor_voltaire(db_conection: Cursor):
    '''
    Teste excluir autor voltaire
    pytest tests/db/test_autor.py::test_excluir_autor_voltaire -vv
    '''
    voltaire = 'voltaire'
    try:
        autor = get_autor_by_nome(db_conection, voltaire)
        assert autor
        identificacao: int = autor['id']
        delete_autor(db_conection, identificacao)
        autor = get_autor_by_id(db_conection, identificacao)
        assert not autor
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
