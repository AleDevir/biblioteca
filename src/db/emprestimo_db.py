'''
DB emprestimo
'''
from datetime import datetime

from typing import Any
from sqlite3 import Connection, Cursor

from src.util.data_hora_util import converter_timestamp_to_datetime

def drop_table_emprestimos(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS emprestimos")


def criar_tabela_emprestimos(db_conection: Connection)-> None:
    '''
    Cria a tabela emprestimos
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS emprestimos(
                    id integer primary key autoincrement,
                    usuario_id integer NOT NULL,
                    livro_id integer NOT NULL,
                    exemplar_id integer NOT NULL,
                    numero_de_renovacoes integer NOT NULL,
                    estado text NOT NULL,
                    data_emprestimo text NOT NULL,
                    data_para_devolucao text NOT NULL,
                    data_devolucao text,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY(livro_id) REFERENCES livros(id),
                    FOREIGN KEY(exemplar_id) REFERENCES exemplares(id))''')

    db_conection.commit()


def insert_emprestimo(
        db_conection: Connection,
        usuario_id: int,
        livro_id: int,
        exemplar_id: int,
        estado: str,
        data_emprestimo: datetime,
        data_para_devolucao: datetime,
        data_devolucao: datetime | None,
        numero_de_renovacoes: int = 0,
) -> int:
    '''
    Inseri emprestimo na tabela.
    '''
    dados =  (
        usuario_id,
        livro_id,
        exemplar_id,
        numero_de_renovacoes,
        estado,
        data_emprestimo,
        data_para_devolucao,
        data_devolucao
    )

    cursor: Cursor = db_conection.cursor()
    cursor.execute('INSERT INTO emprestimos(usuario_id, livro_id, exemplar_id, numero_de_renovacoes, estado, data_emprestimo, data_para_devolucao, data_devolucao) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', dados) # pylint: disable=line-too-long
    emprestimo_id = cursor.lastrowid
    db_conection.commit()
    return emprestimo_id


def tuple_to_dict(data: tuple) -> dict[str, Any]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    (
        identificacao,
        usuario_id,
        livro_id,
        exemplar_id,
        numero_de_renovacoes,
        estado,
        data_emprestimo,
        data_para_devolucao,
        data_devolucao
     ) =  data
    return {
        'id': identificacao,
        'usuario_id': usuario_id,
        'livro_id': livro_id,
        'exemplar_id': exemplar_id,
        'numero_de_renovacoes': numero_de_renovacoes,
        'estado': estado,
        'data_emprestimo': converter_timestamp_to_datetime(data_emprestimo),
        'data_para_devolucao': converter_timestamp_to_datetime(data_para_devolucao),
        'data_devolucao': converter_timestamp_to_datetime(data_devolucao) if data_devolucao else None,
    }


def get_emprestimo_by_id(db_conection: Connection, emprestimo_id: int) -> dict[str, Any]:
    '''
    Obter um emprestimo pelo id.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, usuario_id, livro_id, exemplar_id, numero_de_renovacoes, estado, data_emprestimo, data_para_devolucao, data_devolucao FROM emprestimos WHERE id = {emprestimo_id} ")
    data = cursor.fetchone()
    return tuple_to_dict(data)


def get_emprestimos(db_conection: Connection) -> list[dict[str, Any]]:
    '''
    Obter TODOS os emprestimos
    '''
    cursor = db_conection.cursor()
    cursor.execute('SELECT id, usuario_id, livro_id, exemplar_id, numero_de_renovacoes, estado, data_emprestimo, data_para_devolucao, data_devolucao FROM emprestimos')
    emprestimo_db = cursor.fetchall()
    result: list[dict[str, Any]] = []
    for data in emprestimo_db:
        emprestimo = tuple_to_dict(data)
        result.append(emprestimo)
    return result


#################################################
    # UPDATE - EMPRESTIMO #
#################################################

def update_emprestimo_devolucao(
        db_conection: Connection,
        identificacao: int,
        estado: str,
        data_devolucao: datetime | None,        
    ) -> None:
    '''
    Atualiza dados do emprestimo na tabela.
    '''
    dados = (estado, data_devolucao, identificacao)
    print('.........................')
    print(dados)
    print('.........................')
    db_conection.cursor().execute("UPDATE emprestimos SET estado = ?, data_devolucao = ? WHERE id = ?", dados) # pylint: disable=line-too-long
    db_conection.commit()


def update_emprestimo_renovacao(
        db_conection: Connection,
        identificacao: int,
        numero_de_renovacoes: int,
        data_para_devolucao: datetime | None,        
    ) -> None:
    '''
    Atualiza dados do emprestimo na tabela.
    '''
    dados = (numero_de_renovacoes, data_para_devolucao, identificacao)
    print('.........................')
    print(dados)
    print('.........................')
    db_conection.cursor().execute("UPDATE emprestimos SET numero_de_renovacoes = ?, data_para_devolucao = ? WHERE id = ?", dados) # pylint: disable=line-too-long
    db_conection.commit()

#################################################
    # DELETE - EMPRESTIMO #
#################################################
def delete_emprestimo(db_conection: Connection, identificacao: int):
    '''
    Deleta um emprestimo de id informado.
    '''
    db_conection.cursor().execute("DELETE FROM emprestimos WHERE id= ?", (str(identificacao)))
    db_conection.commit()
