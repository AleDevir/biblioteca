'''
Módulo Livro repositório
'''

from sqlite3 import Connection

from src.db.autor_db import get_autores
from src.db.autor_livro_db import get_by_livro
from src.db.livro_db import get_livro_by_id, get_livro_by_titulo
from src.db.editora_db import get_editora_by_id
from src.db.exemplar_db import get_exemplares_by_livro

from src.model.autor import Autor
from src.model.livro import Livro
from src.model.exemplar import Exemplar

def get_livro_por_id(conexao: Connection, livro_id: int) -> Livro:
    '''
    Obtem o livro por título.
    Retorna o livro.
    '''
    livro = get_livro_by_id(conexao, livro_id)
    if not livro:
        raise ValueError(f'\tO livro |{livro_id}| não faz parte do acervo da Biblioteca.')

    editora = get_editora_by_id(conexao, livro.get('editora_id', 0))
    exemplares_list = get_exemplares_by_livro(conexao, livro.get('editora_id', 0))
    exemplares: list[Exemplar] = []
    for dados_exemplar in exemplares_list:
        exemplar = Exemplar(
            identificacao=dados_exemplar.get('id', 0),
            disponivel=dados_exemplar.get('disponivel', 0),
        )
        exemplares.append(exemplar)

    autores_ids = [a['autor_id'] for a in get_by_livro(conexao, livro.get('id', 0))]

    autores_list = [a for a in get_autores(conexao) if a['id'] in autores_ids]
    autores: list[Autor] = []
    for dados_autor in autores_list:
        autor = Autor(
            identificacao=dados_autor.get('id', 0),
            nome=dados_autor.get('nome', 0),
        )
        autores.append(autor)

    return Livro(
        identificacao=livro.get('id', 0),
        titulo=livro.get('titulo', ''),
        renovacoes_permitidas=livro.get('renovacoes_permitidas', 0),
        editora=editora.get('nome', ''),
        generos=[],
        exemplares=exemplares,
        autores=autores,
    )


def get_livro_por_titulo(conexao: Connection, titulo_livro: str) -> Livro:
    '''
    Obtem o livro por título.
    Retorna o livro.
    '''
    livro = get_livro_by_titulo(conexao, titulo_livro.lower())
    if not livro:
        raise ValueError(f'\tO livro |{titulo_livro}| não faz parte do acervo da Biblioteca.')

    editora = get_editora_by_id(conexao, livro.get('editora_id', 0))
    exemplares_list = get_exemplares_by_livro(conexao, livro.get('editora_id', 0))
    exemplares: list[Exemplar] = []
    for dados_exemplar in exemplares_list:
        exemplar = Exemplar(
            identificacao=dados_exemplar.get('id', 0),
            disponivel=dados_exemplar.get('disponivel', 0),
        )
        exemplares.append(exemplar)

    autores_ids = [a['autor_id'] for a in get_by_livro(conexao, livro.get('id', 0))]

    autores_list = [a for a in get_autores(conexao) if a['id'] in autores_ids]
    autores: list[Autor] = []
    for dados_autor in autores_list:
        autor = Autor(
            identificacao=dados_autor.get('id', 0),
            nome=dados_autor.get('nome', 0),
        )
        autores.append(autor)

    return Livro(
        identificacao=livro.get('id', 0),
        titulo=livro.get('titulo', ''),
        renovacoes_permitidas=livro.get('renovacoes_permitidas', 0),
        editora=editora.get('nome', ''),
        generos=[],
        exemplares=exemplares,
        autores=autores,
    )
