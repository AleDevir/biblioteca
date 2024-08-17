'''
Repositório autor
'''
from typing import Any
from sqlite3 import Connection


def drop_table_autores(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS autores")


def criar_tabela_autores(db_conection: Connection)-> None:
    '''
    Cria a tabela autores
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS autores(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL)''')

    db_conection.commit()


def insert_autor(db_conection: Connection, nome: str) -> None:
    '''
    Inseri autor na tabela.
    '''
    db_conection.cursor().execute("INSERT INTO autores(nome) VALUES(?)", (nome,))
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


def get_autor_by_id(db_conection: Connection, autor_id: int) -> dict[str, Any]:
    '''
    Obter um autor pelo id.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, nome FROM autores WHERE id = {autor_id} ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_autor_by_nome(db_conection: Connection, autor_nome: str) -> dict[str, Any]:
    '''
    Obter um Autor pelo nome.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, nome FROM autores WHERE nome = '{autor_nome}' ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_autores(db_conection: Connection) -> list[dict[str, Any]]:
    '''
    Obter TODOS os autores
    '''
    cursor = db_conection.cursor()
    cursor.execute('SELECT id, nome FROM autores')
    autores_db = cursor.fetchall()
    result: list[dict[str, Any]] = []
    for data in autores_db:
        autor = tuple_to_dict(data)
        result.append(autor)
    return result

#################################################
    # UPDATE - AUTOR #
#################################################
def update_autor(db_conection: Connection, autor_nome: str,  autor_id: str) -> None:
    '''
    Atualiza dados do autor na tabela.
    '''
    db_conection.cursor().execute("UPDATE autores SET nome = ?  WHERE id = ?", (autor_nome, autor_id))
    db_conection.commit()


#################################################
    # DELETE - AUTOR #
#################################################
def delete_autor(db_conection: Connection, identificacao: int):
    '''
    Deleta um autor de id informado.
    '''
    db_conection.cursor().execute("DELETE FROM autores WHERE id= ?", (str(identificacao)))
    db_conection.commit()
