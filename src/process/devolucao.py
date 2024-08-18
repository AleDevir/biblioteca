'''
Realizar Devolução
Fluxo para a devolução de um empréstimo.
'''
from sqlite3 import Connection

from src.db.emprestimo_db import update_emprestimo_devolucao
from src.db.exemplar_db import update_exemplar
from src.montagem.emprestimo_montagem import montar_emprestimo_por_id

from src.model.emprestimo import Emprestimo

def devolver_emprestimo(conexao: Connection, identificacao_emprestimo: int) -> Emprestimo:
    '''
    Devolve a biblioteca o livro (identificação do empréstimo) de título 
    emprestado para o usuário de nome.
    Retorna o Emprestimo.
    '''
    emprestimo: Emprestimo = montar_emprestimo_por_id(conexao, identificacao_emprestimo)
    emprestimo.devolver()
    update_emprestimo_devolucao(
        db_conection=conexao,
        identificacao=emprestimo.identificacao,
        estado=emprestimo.estado,
        data_devolucao=emprestimo.data_devolucao,
    )
    update_exemplar(
        db_conection=conexao,
        disponivel=emprestimo.exemplar.disponivel,
        identificacao=emprestimo.exemplar.identificacao,
    )
    return emprestimo
