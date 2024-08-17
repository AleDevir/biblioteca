'''
Repositório editora
'''
from typing import Any
from sqlite3 import Connection


def drop_table_editoras(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS editoras")


def criar_tabela_editoras(db_conection: Connection)-> None:
    '''
    Cria a tabela editoras
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS editoras(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL)''')

    db_conection.commit()


def insert_editora(db_conection: Connection, nome: str) -> None:
    '''
    Inseri editora na tabela.
    '''
    db_conection.cursor().execute("INSERT INTO editoras(nome) VALUES(?)", (nome,))
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


def get_editora_by_id(db_conection: Connection, editora_id: int) -> dict[str, Any]:
    '''
    Obter uma editora pelo id.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, nome FROM editoras WHERE id = {editora_id} ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_editora_by_nome(db_conection: Connection, editora_nome: str) -> dict[str, Any]:
    '''
    Obter uma editora pelo nome.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, nome FROM editoras WHERE nome = '{editora_nome}' ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_editoras(db_conection: Connection) -> list[dict[str, Any]]:
    '''
    Obter TODOS os editoras
    '''
    cursor = db_conection.cursor()
    cursor.execute('SELECT id, nome FROM editoras')
    editoras_db = cursor.fetchall()
    result: list[dict[str, Any]] = []
    for data in editoras_db:
        editora = tuple_to_dict(data)
        result.append(editora)
    return result

#################################################
    # UPDATE - editora #
#################################################
def update_editora(db_conection: Connection, editora_nome: str,  editora_id: str) -> None:
    '''
    Atualiza dados do editora na tabela.
    '''
    db_conection.cursor().execute("UPDATE editoras SET nome = ?  WHERE id = ?", (editora_nome, editora_id))
    db_conection.commit()


#################################################
    # DELETE - editora #
#################################################
def delete_editora(db_conection: Connection, identificacao: int):
    '''
    Deleta uma editora de id informado.
    '''
    db_conection.cursor().execute("DELETE FROM editoras WHERE id= ?", (str(identificacao)))
    db_conection.commit()
