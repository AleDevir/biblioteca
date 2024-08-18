'''
DB generos_livros
'''
from sqlite3 import Connection


def drop_table_generos_livros(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já existir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS generos_livros")


def criar_tabela_generos_livros(db_conection: Connection)-> None:
    '''
    Cria a tabela generos_livros
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS generos_livros(
                    genero_id integer NOT NULL,
                    livro_id interger NOT NULL,
                    PRIMARY KEY (livro_id, genero_id),
                    FOREIGN KEY(livro_id) REFERENCES livros(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY(genero_id) REFERENCES generos(id)
                        ON DELETE RESTRICT)''')

    db_conection.commit()


def insert_generos_livros(db_conection: Connection, genero_id: int, livro_id: int) -> None:
    '''
    Inseri genero_id e livro_id na tabela.
    '''
    dados = (genero_id, livro_id)
    db_conection.cursor().execute('INSERT INTO generos_livros(genero_id, livro_id) VALUES(?, ?)', dados)
    db_conection.commit()


def tuple_to_dict(data: tuple) -> dict[str, int]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    genero_id, livro_id, genero_nome =  data
    return {
        'genero_id': genero_id,
        'livro_id': livro_id,
        'genero_nome': genero_nome,
    }

def get_by_pk(
    db_conection: Connection,
    genero_id: int,
    livro_id: int,
) -> dict[str, int]:
    '''
    Obter um
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"""SELECT al.genero_id, al.livro_id, generos.nome as genero_nome
                   FROM generos_livros AS al
                   INNER JOIN generos ON (al.genero_id = generos.id)
                   WHERE
                    al.genero_id = {genero_id}
                    AND
                    al.livro_id = {livro_id} """)
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_generos_by_genero_id(db_conection: Connection, genero_id: int) -> list[dict[str, int]]:
    '''
    Obter TODOS os generos
    '''
    cursor = db_conection.cursor()
    # cursor.execute(f"SELECT genero_id, livro_id FROM generos_livros WHERE genero_id = {genero_id} ")
    cursor.execute(f"""SELECT al.genero_id, al.livro_id, generos.nome as genero_nome
                   FROM generos_livros AS al
                   INNER JOIN generos ON (al.genero_id = generos.id)
                   WHERE
                    al.genero_id = {genero_id} """)
    generos_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in generos_db:
        genero = tuple_to_dict(data)
        result.append(genero)
    return result


def get_generos_by_livro_id(db_conection: Connection, livro_id: int) -> list[dict[str, int]]:
    '''
    Obter TODOS os livros
    '''
    cursor = db_conection.cursor()
    # cursor.execute(f"SELECT genero_id, livro_id FROM generos_livros WHERE livro_id = {livro_id} ")
    cursor.execute(f"""SELECT al.genero_id, al.livro_id, generos.nome as genero_nome
                   FROM generos_livros AS al
                   INNER JOIN generos ON (al.genero_id = generos.id)
                   WHERE
                    al.livro_id = {livro_id} """)
    generos_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in generos_db:
        genero = tuple_to_dict(data)
        result.append(genero)
    return result


def delete_generos_livros(db_conection: Connection, genero_id: int, livro_id: int):
    '''
    Deleta uma linha da tabela.
    '''
    db_conection.cursor().execute("DELETE FROM generos_livros WHERE genero_id= ? AND livro_id=? ", (str(genero_id), str(livro_id)))
    db_conection.commit()


def delete_genero(db_conection: Connection, genero_id: int):
    '''
    Deleta uma linha da tabela.
    '''
    dados = (genero_id,)
    db_conection.cursor().execute("DELETE FROM generos_livros WHERE genero_id= ? ", dados)
    db_conection.commit()
