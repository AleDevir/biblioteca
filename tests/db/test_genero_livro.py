'''
Teste do genero livro DB
pytest tests/db/test_genero_livro.py -vv
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.genero_livro_db import (
    get_generos_by_genero_id,
    get_generos_by_livro_id,
    get_by_pk,
    insert_generos_livros,
    delete_generos_livros,
    delete_genero,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


@pytest.mark.parametrize('genero_id,livros_ids', [
    # genero_id, list(livro_id)
    (1, [1,2,3,4]),
    (2, [2,3,4]),
    (3, [3,4]),
])
def test_get_by_genero(
    db_conection: Cursor,
    genero_id: int,
    livros_ids: list[int]
):
    '''
    Teste carga
    pytest tests/db/test_genero_livro.py::test_get_by_genero -vv
    '''
    try:
        dados = get_generos_by_genero_id(db_conection, genero_id)
        assert dados
        assert isinstance(dados, list)
        assert len(dados) == len(livros_ids)
        for dado in dados:
            assert dado
            assert isinstance(dado, dict)
            assert 'genero_id' in dado
            assert 'livro_id' in dado
            assert dado['genero_id'] == genero_id
            assert dado['livro_id'] in livros_ids
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()

@pytest.mark.parametrize('livro_id,generos_ids', [
    # livro_id, list(genero_id)
    (1, [1]),
    (2, [1,2]),
    (3, [1,2,3]),
])
def test_get_by_livro(
    db_conection: Cursor,
    livro_id: int,
    generos_ids: list[int]
):
    '''
    Teste carga
    pytest tests/db/test_genero_livro.py::test_get_by_livro -vv
    '''
    try:
        dados = get_generos_by_livro_id(db_conection, livro_id)
        assert dados
        assert isinstance(dados, list)
        assert len(dados) == len(generos_ids)
        for dado in dados:
            assert dado
            assert isinstance(dado, dict)
            assert 'genero_id' in dado
            assert 'livro_id' in dado
            assert dado['livro_id'] == livro_id
            assert dado['genero_id'] in generos_ids
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_add(db_conection: Cursor):
    '''
    Teste inserir
    pytest tests/db/test_genero_livro.py::test_add -vv
    '''
    genero_id = 2
    livro_id = 1
    try:
        insert_generos_livros(
            db_conection,
            genero_id=genero_id,
            livro_id=livro_id
        )
        # Um registro
        um_registro = get_by_pk(
            db_conection=db_conection,
            genero_id=genero_id,
            livro_id=livro_id
        )
        assert um_registro
        assert 'genero_id' in um_registro
        assert 'livro_id' in um_registro
        assert um_registro['genero_id'] == genero_id
        assert um_registro['livro_id'] == livro_id

        # por generos
        por_generos = get_generos_by_genero_id(db_conection, genero_id)
        assert por_generos
        for dado in por_generos:
            assert dado['genero_id'] == genero_id

        # por Livros
        por_livros = get_generos_by_livro_id(db_conection, livro_id)
        assert por_livros
        for dado in por_livros:
            assert dado['livro_id'] == livro_id
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir(db_conection: Cursor):
    '''
    Teste excluir
    pytest tests/db/test_genero_livro.py::test_excluir -vv
    '''
    genero_id = 2
    livro_id = 1
    try:
        um_registro = get_by_pk(
            db_conection=db_conection,
            genero_id=genero_id,
            livro_id=livro_id
        )
        assert um_registro
        delete_generos_livros(
            db_conection=db_conection,
            genero_id=genero_id,
            livro_id=livro_id
        )
        um_registro = get_by_pk(
            db_conection=db_conection,
            genero_id=genero_id,
            livro_id=livro_id
        )
        assert not um_registro
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
