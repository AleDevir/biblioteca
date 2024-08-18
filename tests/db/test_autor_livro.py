'''
Teste do autor livro DB
pytest tests/db/test_autor_livro.py -vv
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.autor_livro_db import (
    get_autores_by_autor_id,
    get_autores_by_livro_id,
    get_by_pk,
    insert_autores_livros,
    delete_autores_livros,
    delete_autor,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


@pytest.mark.parametrize('autor_id,livros_ids', [
    # autor_id, list(livro_id)
    (1, [1,2,3,4]),
    (2, [2,3,4]),
    (3, [3,4]),
])
def test_get_by_autor(
    db_conection: Cursor,
    autor_id: int,
    livros_ids: list[int]
):
    '''
    Teste carga
    pytest tests/db/test_autor_livro.py::test_get_by_autor -vv
    '''
    try:
        dados = get_autores_by_autor_id(db_conection, autor_id)
        assert dados
        assert isinstance(dados, list)
        assert len(dados) == len(livros_ids)
        for dado in dados:
            assert dado
            assert isinstance(dado, dict)
            assert 'autor_id' in dado
            assert 'livro_id' in dado
            assert dado['autor_id'] == autor_id
            assert dado['livro_id'] in livros_ids
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()

@pytest.mark.parametrize('livro_id,autores_ids', [
    # livro_id, list(autor_id)
    (1, [1]),
    (2, [1,2]),
    (3, [1,2,3]),
])
def test_get_by_livro(
    db_conection: Cursor,
    livro_id: int,
    autores_ids: list[int]
):
    '''
    Teste carga
    pytest tests/db/test_autor_livro.py::test_get_by_livro -vv
    '''
    try:
        dados = get_autores_by_livro_id(db_conection, livro_id)
        assert dados
        assert isinstance(dados, list)
        assert len(dados) == len(autores_ids)
        for dado in dados:
            assert dado
            assert isinstance(dado, dict)
            assert 'autor_id' in dado
            assert 'livro_id' in dado
            assert dado['livro_id'] == livro_id
            assert dado['autor_id'] in autores_ids
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_add(db_conection: Cursor):
    '''
    Teste inserir
    pytest tests/db/test_autor_livro.py::test_add -vv
    '''
    autor_id = 2
    livro_id = 1
    try:
        insert_autores_livros(
            db_conection,
            autor_id=autor_id,
            livro_id=livro_id
        )
        # Um registro
        um_registro = get_by_pk(
            db_conection=db_conection,
            autor_id=autor_id,
            livro_id=livro_id
        )
        assert um_registro
        assert 'autor_id' in um_registro
        assert 'livro_id' in um_registro
        assert um_registro['autor_id'] == autor_id
        assert um_registro['livro_id'] == livro_id

        # por Autores
        por_autores = get_autores_by_autor_id(db_conection, autor_id)
        assert por_autores
        for dado in por_autores:
            assert dado['autor_id'] == autor_id

        # por Livros
        por_livros = get_autores_by_livro_id(db_conection, livro_id)
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
    pytest tests/db/test_autor_livro.py::test_excluir -vv
    '''
    autor_id = 2
    livro_id = 1
    try:
        um_registro = get_by_pk(
            db_conection=db_conection,
            autor_id=autor_id,
            livro_id=livro_id
        )
        assert um_registro
        delete_autores_livros(
            db_conection=db_conection,
            autor_id=autor_id,
            livro_id=livro_id
        )
        um_registro = get_by_pk(
            db_conection=db_conection,
            autor_id=autor_id,
            livro_id=livro_id
        )
        assert not um_registro
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
