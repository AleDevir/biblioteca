'''
Teste do livro DB
'''

import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.livro_db import (
    get_livros,
    get_livro_by_id,
    get_livro_by_titulo,
    insert_livro,
    update_livro,
    delete_livro,
)
from src.db.autor_livro_db import get_by_livro
from src.db.exemplar_db import get_exemplares_by_livro


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_get_livros(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_livro.py::test_get_livros -vv
    '''
    try:
        livros = get_livros(db_conection)
        assert livros
        assert isinstance(livros, list)
        assert len(livros) == 4
        for indice, livro in enumerate(livros):
            assert livro
            assert isinstance(livro, dict)
            assert 'id' in livro
            assert 'titulo' in livro
            assert livro['id'] == indice + 1
            assert livro['titulo'] == f'livro{indice + 1}'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_get_livro_by_id_inexistente(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_livro.py::test_get_livro_by_id_inexistente -vv
    '''
    identificacao = 999
    try:
        livro = get_livro_by_id(db_conection, identificacao)
        assert not livro
        assert isinstance(livro, dict)
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('identificacao', [1,2,3])
def test_get_livro_by_id(db_conection: Cursor, identificacao: int):
    '''
    Teste carga
    pytest tests/db/test_livro.py::test_get_livro_by_id -vv
    '''
    try:
        livro = get_livro_by_id(db_conection, identificacao)
        assert livro
        assert isinstance(livro, dict)
        assert 'id' in livro
        assert 'titulo' in livro
        assert 'renovacoes_permitidas' in livro
        assert 'editora_id' in livro
        assert livro['id'] == identificacao
        assert livro['titulo'] == f'livro{identificacao}'
        assert livro['renovacoes_permitidas'] == identificacao - 1
        assert livro['editora_id'] == identificacao
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('titulo', ['livro1','livro2','livro3'])
def test_get_livro_by_titulo(db_conection: Cursor, titulo: str):
    '''
    Teste carga
    pytest tests/db/test_livro.py::test_get_livro_by_titulo -vv
    '''
    try:
        livro = get_livro_by_titulo(db_conection, titulo)
        assert livro
        assert isinstance(livro, dict)
        assert 'id' in livro
        assert 'titulo' in livro
        assert 'renovacoes_permitidas' in livro
        assert 'editora_id' in livro
        assert livro['titulo'] == titulo
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_livro_4(db_conection: Cursor):
    '''
    Teste excluir livro 4
    pytest tests/db/test_livro.py::test_excluir_livro_4 -vv
    '''
    identificacao = 4
    try:
        delete_livro(db_conection, identificacao)
        livro = get_livro_by_id(db_conection, identificacao)
        assert not livro
        autores = get_by_livro(db_conection, identificacao)
        assert not autores
        exemplares = get_exemplares_by_livro(db_conection, identificacao)
        assert not exemplares
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_criar_livro_fausto(db_conection: Cursor):
    '''
    Teste criar livro
    pytest tests/db/test_livro.py::test_criar_livro_fausto -vv
    '''
    fausto = 'fausto'
    renovacoes_permitidas = 5
    editora_id = 1
    try:
        insert_livro(db_conection, fausto, renovacoes_permitidas, editora_id)
        livro = get_livro_by_titulo(db_conection, fausto)
        assert livro
        assert livro['titulo'] == fausto
        assert livro['renovacoes_permitidas'] == renovacoes_permitidas
        assert livro['editora_id'] == editora_id
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_alterar_livro_fausto(db_conection: Cursor):
    '''
    Teste alterar livro fausto
    pytest tests/db/test_livro.py::test_alterar_livro_fausto -vv
    '''
    fausto = 'fausto'
    titulo_alterado = fausto + ' ALTERADO'
    renovacoes_permitidas = 10
    editora_id = 2
    try:
        livro = get_livro_by_titulo(db_conection, fausto)
        assert livro
        identificacao: int = livro['id']
        update_livro(
            db_conection=db_conection,
            titulo=titulo_alterado,
            renovacoes_permitidas=renovacoes_permitidas,
            editora_id=editora_id,
            identificacao=identificacao,
        )
        livro = get_livro_by_id(db_conection, identificacao)
        assert livro
        assert livro['titulo'] == titulo_alterado
        assert livro['renovacoes_permitidas'] == renovacoes_permitidas
        assert livro['editora_id'] == editora_id
        # Voltando com o nome original
        update_livro(
            db_conection=db_conection,
            titulo=fausto,
            renovacoes_permitidas=renovacoes_permitidas,
            editora_id=editora_id,
            identificacao=identificacao,
        )
        livro = get_livro_by_titulo(db_conection, fausto)
        assert livro
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_livro_fausto(db_conection: Cursor):
    '''
    Teste excluir livro fausto
    pytest tests/db/test_livro.py::test_excluir_livro_fausto -vv
    '''
    fausto = 'fausto'
    try:
        livro = get_livro_by_titulo(db_conection, fausto)
        assert livro
        identificacao: int = livro['id']
        delete_livro(db_conection, identificacao)
        livro = get_livro_by_id(db_conection, identificacao)
        assert not livro
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
