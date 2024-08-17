'''
Módulo livro DB
'''

from typing import Any
from sqlite3 import Connection


def drop_table_livros(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS livros")


def criar_tabela_livros(db_conection: Connection)-> None:
    '''
    Cria a tabela livros
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS livros(
                    id integer primary key autoincrement,
                    titulo text NOT NULL,
                    renovacoes_permitidas integer NOT NULL,                  
                    editora_id integer NOT NULL,
                    FOREIGN KEY(editora_id) REFERENCES editoras(id)
                   )''')


    db_conection.commit()


def insert_livro(
    db_conection: Connection,
    titulo: str,
    renovacoes_permitidas: int,
    editora_id: int
) -> None:
    '''
    Inseri livro na tabela.
    '''
    dados =  (
        titulo,
        renovacoes_permitidas,
        editora_id
    )
    db_conection.cursor().execute('INSERT INTO livros(titulo, renovacoes_permitidas, editora_id) VALUES(?, ?, ?)', dados) # pylint: disable=line-too-long
    db_conection.commit()


def tuple_to_dict(data: tuple) -> dict[str, Any]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, titulo, renovacoes_permitidas,  editora_id  =  data
    return {
        'id': identificacao,
        'titulo': titulo,
        'renovacoes_permitidas': renovacoes_permitidas,
        'editora_id': editora_id,
    }


def get_livro_by_id(db_conection: Connection, livro_id: int) -> dict[str, Any]:
    '''
    Obter um livro pelo id.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, titulo, renovacoes_permitidas, editora_id FROM livros WHERE id = {livro_id} ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_livro_by_titulo(db_conection: Connection, titulo: str) -> dict[str, Any]:
    '''
    Obter um livro pelo titulo.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, titulo, renovacoes_permitidas, editora_id FROM livros WHERE titulo = '{titulo}' ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_livros(db_conection: Connection) -> list[dict[str, Any]]:
    '''
    Obter TODOS os Livros
    '''
    cursor = db_conection.cursor()
    cursor.execute('SELECT id, titulo, renovacoes_permitidas, editora_id FROM livros')
    livro_db = cursor.fetchall()
    result: list[dict[str, Any]] = []
    for data in livro_db:
        livro = tuple_to_dict(data)
        result.append(livro)
    return result

#################################################
    # UPDATE - LIVRO #
#################################################

def update_livro(
        db_conection: Connection,
        titulo: str,
        renovacoes_permitidas: int,
        editora_id: int,
        identificacao: int,
    ) -> None:
    '''
    Atualiza dados do livro na tabela.
    '''
    db_conection.cursor().execute("UPDATE livros SET titulo = ?, renovacoes_permitidas = ?, editora_id = ?  WHERE id = ?", (titulo, renovacoes_permitidas, editora_id, identificacao)) # pylint: disable=line-too-long
    db_conection.commit()

#################################################
    # DELETE - LIVRO #
#################################################
def delete_livro(db_conection: Connection, identificacao: int):
    '''
    Deleta um livro de id informado.
    '''
    db_conection.cursor().execute("DELETE FROM livros WHERE id= ?", (str(identificacao)))
    db_conection.commit()
