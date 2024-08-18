'''
DB genero
'''
from typing import Any
from sqlite3 import Connection


def drop_table_generos(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS generos")


def criar_tabela_generos(db_conection: Connection)-> None:
    '''
    Cria a tabela generos
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS generos(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL)''')

    db_conection.commit()


def insert_genero(db_conection: Connection, nome: str) -> None:
    '''
    Inseri genero na tabela.
    '''
    db_conection.cursor().execute("INSERT INTO generos(nome) VALUES(?)", (nome,))
    db_conection.commit()


def tuple_to_dict(data: tuple) -> dict[str, Any]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, nome =  data
    return {
        'id': identificacao,
        'nome': nome,
    }


def get_genero_by_id(db_conection: Connection, genero_id: int) -> dict[str, Any]:
    '''
    Obter um genero pelo id.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, nome FROM generos WHERE id = {genero_id} ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_genero_by_nome(db_conection: Connection, genero_nome: str) -> dict[str, Any]:
    '''
    Obter um genero pelo nome.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, nome FROM generos WHERE nome = '{genero_nome}' ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_generos(db_conection: Connection) -> list[dict[str, Any]]:
    '''
    Obter TODOS os generos
    '''
    cursor = db_conection.cursor()
    cursor.execute('SELECT id, nome FROM generos')
    generos_db = cursor.fetchall()
    result: list[dict[str, Any]] = []
    for data in generos_db:
        genero = tuple_to_dict(data)
        result.append(genero)
    return result

#################################################
    # UPDATE - genero #
#################################################
def update_genero(db_conection: Connection, genero_nome: str,  genero_id: str) -> None:
    '''
    Atualiza dados do genero na tabela.
    '''
    db_conection.cursor().execute("UPDATE generos SET nome = ?  WHERE id = ?", (genero_nome, genero_id))
    db_conection.commit()


#################################################
    # DELETE - genero #
#################################################
def delete_genero(db_conection: Connection, identificacao: int):
    '''
    Deleta um genero de id informado.
    '''
    db_conection.cursor().execute("DELETE FROM generos WHERE id= ?", (str(identificacao)))
    db_conection.commit()
