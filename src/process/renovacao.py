'''
Realizar Renovação do emprestimo
Fluxo para a renovação de um empréstimo.
'''
from sqlite3 import Connection

from src.db.emprestimo_db import update_emprestimo_renovacao

from src.montagem.emprestimo_montagem import montar_emprestimo_por_id

from src.model.emprestimo import Emprestimo

def renovar_emprestimo(conexao: Connection, identificacao_emprestimo: int) -> Emprestimo:
    '''
    Devolve a biblioteca o livro (identificação do empréstimo) de título 
    emprestado para o usuário de nome.
    Retorna o Emprestimo.
    '''
    emprestimo: Emprestimo = montar_emprestimo_por_id(conexao, identificacao_emprestimo)
    emprestimo.renovar()
    update_emprestimo_renovacao(
        db_conection=conexao,
        identificacao=emprestimo.identificacao,
        numero_de_renovacoes=emprestimo.exemplar.numero_de_renovacoes,
        data_para_devolucao=emprestimo.data_para_devolucao,
    )
    return emprestimo
