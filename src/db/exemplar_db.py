'''
Módulo exemplar DB
'''

from sqlite3 import Connection


def drop_table_exemplares(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS exemplares")


def criar_tabela_exemplares(db_conection: Connection)-> None:
    '''
    Cria a tabela exemplares
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS exemplares(
                    id integer primary key autoincrement,
                    disponivel integer NOT NULL,                  
                    livro_id integer NOT NULL,
                    FOREIGN KEY(livro_id) REFERENCES livros(id)
                        ON DELETE CASCADE)''')

    db_conection.commit()


def insert_exemplar(
    db_conection: Connection,
    livro_id: int,
    disponivel: int = 1,
) -> None:
    '''
    Inseri exemplar na tabela.
    '''
    dados =  (
        disponivel,
        livro_id
    )
    db_conection.cursor().execute('INSERT INTO exemplares(disponivel, livro_id) VALUES(?, ?)', dados) # pylint: disable=line-too-long
    db_conection.commit()


def tuple_to_dict(data: tuple) -> dict[str, int]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, disponivel,  livro_id  =  data
    return {
        'id': identificacao,
        'disponivel': disponivel,
        'livro_id': livro_id,
    }


def get_exemplar_by_id(db_conection: Connection, exemplar_id: int) -> dict[str, int]:
    '''
    Obter um exemplar pelo id.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, disponivel, livro_id FROM exemplares WHERE id = {exemplar_id} ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_exemplares_by_livro(db_conection: Connection, livro_id: int) -> list[dict[str, int]]:
    '''
    Obter TODOS os exemplares do livro
    '''
    cursor = db_conection.cursor()
    cursor.execute(f'SELECT id, disponivel, livro_id FROM exemplares WHERE livro_id = {livro_id} ')
    exemplar_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in exemplar_db:
        exemplar = tuple_to_dict(data)
        result.append(exemplar)
    return result


def update_exemplar(
        db_conection: Connection,
        disponivel: int,
        identificacao: int,
    ) -> None:
    '''
    Atualiza dados do exemplar na tabela.
    '''
    db_conection.cursor().execute("UPDATE exemplares SET disponivel = ?  WHERE id = ?", (disponivel, identificacao)) # pylint: disable=line-too-long
    db_conection.commit()

#################################################
    # DELETE - exemplar #
#################################################
def delete_exemplar(db_conection: Connection, identificacao: int):
    '''
    Deleta um exemplar de id informado.
    '''
    db_conection.cursor().execute("DELETE FROM exemplares WHERE id= ?", (str(identificacao),))
    db_conection.commit()
