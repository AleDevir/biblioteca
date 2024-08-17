'''
Teste do Autor DB
pytest tests/db/test__carga.py -vv
'''

import pytest
from sqlite3 import Connection
from src.db.conexao_db import get_conexao_db
from src.db.carga_db import carregar_banco_de_dados


@pytest.fixture(scope='function')
def db_conection() -> Connection:
    '''
    Obtem a conexão do banco de dados de teste.
    '''
    return get_conexao_db('./tests/db/banco_de_dados_de_teste.db')


def test_carga_de_dados(db_conection: Connection):
    '''
    Teste carga
    pytest tests/db/test__carga.py::test_carga_de_dados -vv
    '''
    try:
        carregar_banco_de_dados(db_conection)
        assert True
    except Exception as erro:
        print(erro)
        assert False
    finally:
        db_conection.close()
