'''
Teste do emprestimo DB
pytest tests/db/test_emprestimo.py -vv
'''
from datetime import datetime, timedelta
import pytest
from sqlite3 import Cursor
from src.db.conexao_db import get_conexao_db
from src.db.emprestimo_db import (
    get_emprestimos,
    get_emprestimo_by_id,
    insert_emprestimo,
    update_emprestimo,
    delete_emprestimo,
)


@pytest.fixture(scope='function')
def db_conection() -> Cursor:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_get_emprestimos(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_emprestimo.py::test_get_emprestimos -vv
    '''
    try:
        emprestimos = get_emprestimos(db_conection)
        assert emprestimos
        assert isinstance(emprestimos, list)
        assert len(emprestimos) == 3
        for indice, emprestimo in enumerate(emprestimos):
            assert emprestimo
            assert isinstance(emprestimo, dict)
            assert 'id' in emprestimo
            assert emprestimo['id'] == indice + 1
            assert emprestimo['estado'] == 'DEVOLVIDO'
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_get_emprestimo_by_id_inexistente(db_conection: Cursor):
    '''
    Teste carga
    pytest tests/db/test_emprestimo.py::test_get_emprestimo_by_id_inexistente -vv
    '''
    identificacao = 999
    try:
        emprestimo = get_emprestimo_by_id(db_conection, identificacao)
        assert not emprestimo
        assert isinstance(emprestimo, dict)
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


@pytest.mark.parametrize('identificacao', [1,2,3])
def test_get_emprestimo_by_id(db_conection: Cursor, identificacao: int):
    '''
    Teste carga
    pytest tests/db/test_emprestimo.py::test_get_emprestimo_by_id -vv
    '''
    try:
        emprestimo = get_emprestimo_by_id(db_conection, identificacao)
        assert emprestimo
        assert isinstance(emprestimo, dict)
        assert 'id' in emprestimo
        assert 'estado' in emprestimo
        assert 'numero_de_renovacoes' in emprestimo
        assert 'usuario_id' in emprestimo
        assert 'livro_id' in emprestimo
        assert 'exemplar_id' in emprestimo
        assert emprestimo['id'] == identificacao
        assert emprestimo['estado'] == 'DEVOLVIDO'
        assert emprestimo['numero_de_renovacoes'] == identificacao - 1
        assert emprestimo['usuario_id'] == 1
        assert emprestimo['livro_id'] == identificacao
        assert emprestimo['exemplar_id'] == identificacao
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_add_emprestimo(db_conection: Cursor):
    '''
    Teste criar emprestimo
    pytest tests/db/test_emprestimo.py::test_add_emprestimo -vv
    '''
    usuario_id = 1
    livro_id = 2
    exemplar_id = 1
    try:
        insert_emprestimo(
            db_conection,
            usuario_id=usuario_id,
            livro_id=livro_id,
            exemplar_id=exemplar_id,
            estado='EMPRESTADO',
            data_emprestimo=datetime.now(),
            data_para_devolucao=datetime.now() + timedelta(days=3),
            data_devolucao=None,
            numero_de_renovacoes= 0
        )
        emprestimo = get_emprestimos(db_conection)[-1]
        assert emprestimo
        assert emprestimo['usuario_id'] == usuario_id
        assert emprestimo['livro_id'] == livro_id
        assert emprestimo['exemplar_id'] == exemplar_id
        assert emprestimo['estado'] == 'EMPRESTADO'
        assert emprestimo['data_emprestimo'] is not None
        assert emprestimo['data_para_devolucao'] is not None
        assert emprestimo['data_devolucao'] is None
        assert emprestimo['numero_de_renovacoes'] == 0
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()


def test_excluir_emprestimo(db_conection: Cursor):
    '''
    Teste excluir emprestimo
    pytest tests/db/test_emprestimo.py::test_excluir_emprestimo -vv
    '''
    try:
        emprestimo = get_emprestimos(db_conection)[-1]
        assert emprestimo
        identificacao: int = emprestimo['id']
        delete_emprestimo(db_conection, identificacao)
        emprestimo = get_emprestimo_by_id(db_conection, identificacao)
        assert not emprestimo
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()