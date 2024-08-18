'''
Módulo Livro repositório
'''

from sqlite3 import Connection

from src.db.emprestimo_db import get_emprestimo_by_id

from src.repositorio.livro_repositorio import get_livro_por_id
from src.repositorio.usuario_repositorio import get_usuario_por_id

from src.model.usuario import Usuario
from src.model.livro import Livro
from src.model.exemplar import Exemplar
from src.model.emprestimo import Emprestimo

def get_emprestimo_por_id(conexao: Connection, emprestimo_id: int) -> Emprestimo:
    '''
    Obtem o livro por título.
    Retorna o livro.
    '''
    emprestimo = get_emprestimo_by_id(conexao, emprestimo_id)

    if not emprestimo:
        raise ValueError(f'\tO empréstimo de ID={emprestimo_id} não existe na base de dados.')

    usuario: Usuario = get_usuario_por_id(conexao, emprestimo.get('usuario_id', 0))
    livro: Livro = get_livro_por_id(conexao, emprestimo.get('livro_id', 0))
    exemplar: Exemplar = Exemplar(
        identificacao=emprestimo.get('exemplar_id', 0),
        numero_de_renovacoes=emprestimo.get('numero_de_renovacoes', 0),
    )

    return Emprestimo(
        identificacao=emprestimo.get('id', 0),
        usuario=usuario,
        livro=livro,
        exemplar=exemplar,
        estado=emprestimo.get('estado', ''),
        data_emprestimo=emprestimo.get('data_emprestimo'),
        data_para_devolucao=emprestimo.get('data_para_devolucao'),
        data_devolucao=emprestimo.get('data_devolucao'),
    )
