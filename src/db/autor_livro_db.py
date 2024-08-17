'''
DB autores_livros
'''
from sqlite3 import Connection


def drop_table_autores_livros(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS autores_livros")


def criar_tabela_autores_livros(db_conection: Connection)-> None:
    '''
    Cria a tabela autores_livros
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS autores_livros(
                    autor_id integer NOT NULL,
                    livro_id interger NOT NULL,
                    PRIMARY KEY (livro_id, autor_id),
                    FOREIGN KEY(livro_id) REFERENCES livros(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY(autor_id) REFERENCES autores(id)
                        ON DELETE RESTRICT)''')

    db_conection.commit()


def insert_autores_livros(db_conection: Connection, autor_id: int, livro_id: int) -> None:
    '''
    Inseri autor_id e livro_id na tabela.
    '''
    dados = (autor_id, livro_id)
    db_conection.cursor().execute('INSERT INTO autores_livros(autor_id, livro_id) VALUES(?, ?)', dados)
    db_conection.commit()


def tuple_to_dict(data: tuple) -> dict[str, int]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    autor_id, livro_id =  data
    return {
        'autor_id': autor_id,
        'livro_id': livro_id,
    }

def get_by_pk(
    db_conection: Connection,
    autor_id: int,
    livro_id: int,
) -> dict[str, int]:
    '''
    Obter um
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT autor_id, livro_id FROM autores_livros WHERE autor_id = {autor_id} AND livro_id = {livro_id} ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_by_autor(db_conection: Connection, autor_id: int) -> list[dict[str, int]]:
    '''
    Obter TODOS os autores
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT autor_id, livro_id FROM autores_livros WHERE autor_id = {autor_id} ")
    autores_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in autores_db:
        autor = tuple_to_dict(data)
        result.append(autor)
    return result


def get_by_livro(db_conection: Connection, livro_id: int) -> list[dict[str, int]]:
    '''
    Obter TODOS os livros
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT autor_id, livro_id FROM autores_livros WHERE livro_id = {livro_id} ")
    autores_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in autores_db:
        autor = tuple_to_dict(data)
        result.append(autor)
    return result


def delete_autores_livros(db_conection: Connection, autor_id: int, livro_id: int):
    '''
    Deleta uma linha da tabela.
    '''
    db_conection.cursor().execute("DELETE FROM autores_livros WHERE autor_id= ? AND livro_id=? ", (str(autor_id), str(livro_id)))
    db_conection.commit()


def delete_autor(db_conection: Connection, autor_id: int):
    '''
    Deleta uma linha da tabela.
    '''
    dados = (autor_id,)
    db_conection.cursor().execute("DELETE FROM autores_livros WHERE autor_id= ? ", dados)
    db_conection.commit()
