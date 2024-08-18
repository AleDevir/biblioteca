'''
Aplicação do gerenciamento da Biblioteca.
'''


from typing import Final, Any
from datetime import datetime
import os
import platform
import locale
from sqlite3 import Connection

from src.db.conexao_db import get_conexao_db

from src.model.emprestimo import Emprestimo

from src.process.emprestimo import realizar_emprestimo
from src.process.devolucao import devolver_emprestimo
from src.process.renovacao import renovar_emprestimo

COR_BRANCA: Final[str] = '\033[0;0m'
COR_BRIGHT_AMARELA: Final[str] = '\033[93m'
COR_VERDE: Final[str] = '\033[32m'
COR_BRIGHT_VERMELHA: Final[str] = '\033[91m'
LINHA_TRACEJADA: Final[str] = '-' * 31
LINHA_PONTILHADA: Final[str] = '-' * 61

OPCOES:  Final[dict[str, str ]] = {
    'E': 'Emprestar',
    'D': 'Devolver',
    'R': 'Renovar',
    'S': 'Sair'    
}


###########################################################
                  # INFRAESTRUTURA #
###########################################################

# Habilita os caracteres ANSI escape no terminal Windows.
os.system("")

def bright_amarelo(conteudo: Any) -> Any:
    '''
    Colore o texto informado em amarelo brilhante.
    Retorna o texto colorido.
    '''
    return f"{COR_BRIGHT_AMARELA}{conteudo}{COR_BRANCA}"

def verde(conteudo: Any) -> Any:
    '''
    Colore o texto informado em verde.
    Retorna o texto colorido.
    '''
    return f"{COR_VERDE}{conteudo}{COR_BRANCA}"

def bright_vermelho(conteudo: Any) -> Any:
    '''
    Colore o texto informado em vermelho brilhante.
    Retorna o texto colorido.
    '''
    return f"{COR_BRIGHT_VERMELHA}{conteudo}{COR_BRANCA}"

def limpar_console():
    '''
    Limpa o console de acordo com a plataforma.
    '''
    if platform.system() == 'Windows':
        os.system('cls')
    if platform.system() == 'Linux':
        os.system('clear')

def get_input(msg: str) -> str:
    '''
    Encapsula as chamadas dos inputs.
    Confecionda para poder testar os inputs.
    '''
    return input(msg)

def input_int(msg: str) -> int:
    '''
    Obtem número inteiro informado pelo usuário.
    Retorna o número.
    '''
    while True:
        try:
            return int(get_input(msg))
        except ValueError:
            print(bright_vermelho('\n\tApenas números inteiros são aceitos. Por favor, tente novamente.\n')) # pylint: disable=line-too-long

def input_opcoes(msg: str, opcoes: dict[str]) -> str:
    '''
    Obtem a opção válida.
    Retorna a opção.
    '''
    while True:
        opcao = get_input(msg).upper()
        if opcao in opcoes:
            return opcao
        print(f"\n\t'{bright_vermelho(opcao)}' opção inválida! As opções válidas são: {verde(', '.join(opcoes))}") # pylint: disable=line-too-long

def datetime_para_str(date_and_time: datetime | None) -> str:
    '''
    Converter data e hora em representação local.
    '''
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    if date_and_time is None:
        return ''
    return f"{date_and_time:%x} às {date_and_time:%X}"

def exibir_menu(opcoes: dict[str, str]) -> None:
    '''
    Exibi o menu de opções.
    '''
    print('')
    print(verde(f'\t{LINHA_TRACEJADA}'))
    cabecalho = 'MENU DE OPÇÕES \n'
    print(verde(cabecalho.center(50)))

    for key, value in opcoes.items():
        opcao = '|' + key + '|' + "  "  + value
        print(f"\t\t{verde(opcao)} ")
    print(verde(f'\t{LINHA_TRACEJADA}'))

def escolher_uma_opcao_do_menu_entrada(opcoes_menu_dict: dict[str, str]) -> str:
    '''
    Escolhe uma opção do menu.
    Retorna uma das opções do menu.
    '''
    exibir_menu(opcoes_menu_dict)
    siglas: list[str] = list(opcoes_menu_dict)
    escolher_opcao = input_opcoes('\n\tEntre com a opção desejada: ', siglas).upper() # pylint: disable=line-too-long
    while escolher_opcao not in siglas:
        escolher_opcao = input_opcoes(
            '\n\tEntre com a opção desejada: ',
             siglas
        ).upper()
    return escolher_opcao

def exibir_ficha(msg: str, emprestimo: Emprestimo) -> None:
    '''
    Exibe a ficha com os dados do emprestimo.
    '''
    print(f"""
                {bright_amarelo(LINHA_PONTILHADA)}
                {bright_amarelo(msg)}
                {bright_amarelo('Identificação do empréstio: ')} {emprestimo.identificacao}
                {bright_amarelo('Nome do usuário: ')}{emprestimo.usuario.nome}
                {bright_amarelo('Título: ')}{emprestimo.livro.titulo}
                {bright_amarelo('Editora: ')}{emprestimo.livro.editora}
                {bright_amarelo('Autor(s): ')}{', '.join([a.nome for a in emprestimo.livro.autores])}
                {bright_amarelo('Gêneros: ')}{', '.join([g.nome for g in emprestimo.livro.generos])}
                {bright_amarelo('Data do empréstimo: ')}{datetime_para_str(emprestimo.data_emprestimo)}
                {bright_amarelo('Data para devolução: ')}{datetime_para_str(emprestimo.data_para_devolucao)}
                {bright_amarelo('Data da devolução do empréstimo: ')}{datetime_para_str(emprestimo.data_devolucao) if emprestimo.data_devolucao else '-'}
                {bright_amarelo('Exemplar: ')}{emprestimo.exemplar.identificacao}
                {bright_amarelo(LINHA_PONTILHADA)}
    """)


###########################################################
                  # DADOS DE ENTRADA #
###########################################################
def get_nome_usuario() -> str:
    '''
    Obtem o nome do usuário e retorna o nome.
    '''
    while True:
        nome = get_input('\n\tEntre com o nome do usuário: ')
        if nome == '':
            print(bright_vermelho('\tValor do nomo inválido. O campo nome deve ser preenchido.'))
        return nome

def get_livro_titulo() -> str:
    '''
    Obtem o livro_titulo do livro e retorna livro_titulo.
    '''
    while True:
        livro_titulo = get_input('\n\tEntre com o título do livro: ')
        if livro_titulo == '':
            print(bright_vermelho('\tValor do nomo inválido. O campo nome deve ser preenchido.'))
        return livro_titulo

###########################################################
                  # EMPRESTAR #
###########################################################
def emprestar(conexao: Connection) -> None:
    '''
    Fluxo do empréstimo
    '''
    try:
        usuario_nome = get_nome_usuario()
        livro_titulo = get_livro_titulo()
        emprestimo: Emprestimo = realizar_emprestimo(conexao, usuario_nome, livro_titulo)
        exibir_ficha('Empréstimo realizado com sucesso! \n', emprestimo)
    except ValueError as erro:
        print(bright_vermelho('\n\tNão foi possível realizar a operação de empréstimo.')) # pylint: disable=line-too-long
        print(bright_vermelho(f'\n\t{str(erro)}'))


###########################################################
                  # RENOVAR #
###########################################################
def renovar(conexao: Connection) -> None:
    '''
    Fluxo do renovar empréstimo
    '''
    try:
        identificacao_emprestimo = input_int('\n\tEntre com a identificação do empréstimo: ')

        emprestimo: Emprestimo = renovar_emprestimo(conexao, identificacao_emprestimo)
        exibir_ficha('Renovação do empréstimo realizada com sucesso! \n', emprestimo)
    except ValueError as erro:
        print(bright_vermelho('\n\tNão foi possível realizar a operação de renovação do empréstimo.')) # pylint: disable=line-too-long
        print(bright_vermelho(f'\n\t{str(erro)}'))


###########################################################
                  # DEVOLVER #
###########################################################
def devolver(conexao: Connection) -> None:
    '''
    Fluxo de devolver empréstimo.
    '''
    try:
        identificacao_emprestimo = input_int('\n\tEntre com a identificação do empréstimo: ')

        emprestimo: Emprestimo = devolver_emprestimo(conexao, identificacao_emprestimo)
        exibir_ficha('Devolução do empréstimo realizada com sucesso! \n', emprestimo)
    except ValueError as erro:
        print(bright_vermelho('\n\tNão foi possível realizar a operação de devolução do empréstimo.')) # pylint: disable=line-too-long
        print(bright_vermelho(f'\n\t{str(erro)}'))


###########################################################
                  # GERENCIAMENTO #
###########################################################
def gerenciamento_biblioteca() -> None:
    '''
    Fluxo Principal do Programa.
    '''
    try:
        conexao: Connection = get_conexao_db()
        limpar_console()
        print(verde('\t*** Gerenciamento da Biblioteca ***\n '))
        while True:
            opcao = escolher_uma_opcao_do_menu_entrada(OPCOES)
            if opcao == 'E':
                emprestar(conexao)
            if opcao == 'D':
                devolver(conexao)
            if opcao == 'R':
                renovar(conexao)
            if opcao == "S":
                print('Sair')
                break
    except Exception as erro:
        print('ERRO!!!')
        print(bright_vermelho(erro))
        raise erro
    finally:
        conexao.close()
