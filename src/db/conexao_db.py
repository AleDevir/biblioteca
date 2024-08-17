'''
Módulo de conexão com a base de dados
'''
from sqlite3 import connect, Connection


def get_conexao_db(filename_db: str = './src/db/banco_de_dados.db') -> Connection:
    '''
    Obtem a conexão com o banco de dados
    '''
    conexao: Connection = connect(filename_db)
    conexao.cursor().execute('PRAGMA foreign_keys=ON;')
    conexao.commit()
    # cursor: Cursor = conexao.cursor()
    return conexao
