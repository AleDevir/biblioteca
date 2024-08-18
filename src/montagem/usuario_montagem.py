'''
Módulo Usuário repositório
'''

from sqlite3 import Connection

from src.db.usuario_db import get_usuario_by_id, get_usuario_by_nome
from src.model.usuario import Usuario


def montar_usuario_por_id(conexao: Connection, usuario_id: int) -> Usuario:
    '''
    Obtem o usuário por ID.
    Retorna o usuário.
    '''
    usuario = get_usuario_by_id(conexao, usuario_id)
    if not usuario:
        raise ValueError(f'\tO usuário de ID={usuario_id} não possui cadastro na Biblioteca.')

    return Usuario(
        identificacao=usuario.get('id', 0),
        nome=usuario.get('nome', ''),
        telefone=usuario.get('telefone', ''),
        nacionalidade=usuario.get('nacionalidade', ''),
    )


def montar_usuario_por_nome(conexao: Connection, nome_usuario: str) -> Usuario:
    '''
    Obtem o usuário por nome.
    Retorna o usuário.
    '''
    usuario = get_usuario_by_nome(conexao, nome_usuario.lower())
    if not usuario:
        raise ValueError(f'\tO usuário |{nome_usuario}| não possui cadastro na Biblioteca.')

    return Usuario(
        identificacao=usuario.get('id', 0),
        nome=usuario.get('nome', ''),
        telefone=usuario.get('telefone', ''),
        nacionalidade=usuario.get('nacionalidade', ''),
    )
