'''
Realizar Emprestimo
Fluxo para a realização de um empréstimo.
'''
from sqlite3 import Connection

from src.db.emprestimo_db import insert_emprestimo
from src.db.exemplar_db import update_exemplar

from src.montagem.livro_montagem import montar_livro_por_titulo
from src.montagem.usuario_montagem import montar_usuario_por_nome

from src.model.emprestimo import Emprestimo
from src.model.usuario import Usuario
from src.model.livro import Livro
from src.model.exemplar import Exemplar

def realizar_emprestimo(conexao: Connection, nome_usuario: str, titulo_livro: str) -> Emprestimo:
    '''
    Empresta ao usuario de nome o livro de título.
    Retorna o empréstimo.
    '''
    usuario: Usuario = montar_usuario_por_nome(conexao, nome_usuario)
    livro: Livro = montar_livro_por_titulo(conexao, titulo_livro)

    if not livro.possui_exemplar_disponivel:
        raise ValueError(f'\tO livro {livro.titulo} não possui exemplares disponíveis para empréstimo.') # pylint: disable=line-too-long

    exemplar: Exemplar = livro.retirar_exemplar()

    emprestimo: Emprestimo = Emprestimo(
        usuario=usuario,
        livro=livro,
        exemplar=exemplar,
    )

    emprestimo_id = insert_emprestimo(
        db_conection=conexao,
        usuario_id=usuario.identificacao,
        livro_id=livro.identificacao,
        exemplar_id=exemplar.identificacao,
        estado=emprestimo.estado,
        data_emprestimo=emprestimo.data_emprestimo,
        data_para_devolucao=emprestimo.data_para_devolucao,
        data_devolucao=emprestimo.data_devolucao,
        numero_de_renovacoes=emprestimo.exemplar.numero_de_renovacoes,
    )

    if emprestimo_id:
        emprestimo.identificacao = emprestimo_id
        update_exemplar(
            db_conection=conexao,
            disponivel=exemplar.disponivel,
            identificacao=exemplar.identificacao,
        )

    return emprestimo
