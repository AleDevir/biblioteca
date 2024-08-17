'''
Teste do exemplar DB
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.exemplar_db import (
    get_exemplares_by_livro,
    get_exemplar_by_id,
    insert_exemplar,
    update_exemplar,
    delete_exemplar,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_get_exemplar_by_id_inexistente(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_exemplar.py::test_get_exemplar_by_id_inexistente -vv
    '''
    identificacao = 999
    try:
        exemplar = get_exemplar_by_id(db_conection, identificacao)
        assert not exemplar
        assert isinstance(exemplar, dict)
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('identificacao', [1,2,3,4,5,6,7,8,9,10])
def test_get_exemplar_by_id(db_conection: Cursor, identificacao: int):
    '''
    Teste carga
    pytest tests/db/test_exemplar.py::test_get_exemplar_by_id -vv
    '''
    try:
        exemplar = get_exemplar_by_id(db_conection, identificacao)
        assert exemplar
        assert isinstance(exemplar, dict)
        assert 'id' in exemplar
        assert 'disponivel' in exemplar
        assert 'livro_id' in exemplar
        assert exemplar['id'] == identificacao
        assert exemplar['disponivel'] == 1
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('livro_id,qtd', [
    # livro_id, quantidade de exemplares do livro)
    (1, 1),
    (2, 2),
    (3, 3),
])
def test_get_exemplares_by_livro(
    db_conection: Cursor,
    livro_id: int,
    qtd: int
):
    '''
    Teste carga
    pytest tests/db/test_exemplar.py::test_get_exemplares_by_livro -vv
    '''
    try:
        exemplares = get_exemplares_by_livro(db_conection, livro_id)
        assert exemplares
        assert isinstance(exemplares, list)
        assert len(exemplares) == qtd
        for exemplar in exemplares:
            assert exemplar
            assert isinstance(exemplar, dict)
            assert 'id' in exemplar
            assert 'disponivel' in exemplar
            assert 'livro_id' in exemplar
            assert exemplar['disponivel'] == 1
            assert exemplar['livro_id'] == livro_id
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_exemplar_10(db_conection: Cursor):
    '''
    Teste excluir exemplar 10
    pytest tests/db/test_exemplar.py::test_excluir_exemplar_10 -vv
    '''
    identificacao = 10
    try:
        delete_exemplar(db_conection, identificacao)
        exemplar = get_exemplar_by_id(db_conection, identificacao)
        assert not exemplar
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_add_exemplar(db_conection: Cursor):
    '''
    Teste criar exemplar
    pytest tests/db/test_exemplar.py::test_add_exemplar -vv
    '''
    livro_id = 4
    try:
        exemplares = get_exemplares_by_livro(db_conection, livro_id)
        insert_exemplar(db_conection, livro_id)
        assert len(exemplares) + 1 == len(get_exemplares_by_livro(db_conection, livro_id))
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_alterar_exemplar_fausto(db_conection: Cursor):
    '''
    Teste alterar exemplar fausto
    pytest tests/db/test_exemplar.py::test_alterar_exemplar_fausto -vv
    '''
    exemplar_id = 9
    try:
        exemplar = get_exemplar_by_id(db_conection, exemplar_id)
        assert exemplar
        assert exemplar['disponivel'] == 1
        identificacao: int = exemplar['id']
        update_exemplar(
            db_conection=db_conection,
            disponivel=0,
            identificacao=identificacao,
        )
        exemplar = get_exemplar_by_id(db_conection, exemplar_id)
        assert exemplar
        assert exemplar['disponivel'] == 0
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
