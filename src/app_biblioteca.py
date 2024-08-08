'''
Aplicação do gerenciamento da Biblioteca.
'''


from typing import Final, Any
from datetime import datetime
import os
import platform
import locale


from src.model.usuario import Usuario
from src.model.emprestimo import Emprestimo
from src.model.livro import Livro
from src.model.exemplar import Exemplar
from src.model.biblioteca import Biblioteca


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

BIBLIOTECA: Final[Biblioteca] = Biblioteca(
    usuarios = [
        Usuario('Ale', '111111111', 'brasileira'),
        Usuario('Elanor', '222222222', 'neozelandes'),
        Usuario('Amana', '333333333', 'brasileira')
    ],
    livros = [
        Livro (
            titulo='Crime e Castigo',
            editora='Martin Claret',
            renovacoes_permitidas=0,
            generos=['Romance', 'Suspense', 'Ficção filosófica'],
            exemplares=[Exemplar(1)],
            autores=['Fiódor Dostoiévski']
        ),
        Livro (
            titulo='Zadig ou o Destino',
            editora='L&PM POCKET',
            renovacoes_permitidas=3,
            generos=['Romance', 'Suspense', 'Ficção filosófica'],
            exemplares=[Exemplar(1)],
            autores=['Voltaire']
        )
    ]
)

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
            print(bright_vermelho('\n\tApenas números inteiros são aceitos. Por favor, tente novamente.\n'))

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
def emprestar() -> None:
    '''
    Fluxo do empréstimo
    '''
    try:
        usuario_nome = get_nome_usuario()
        livro_titulo = get_livro_titulo()
        emprestimo: Emprestimo = BIBLIOTECA.realizar_emprestimo(usuario_nome, livro_titulo)

        nome = emprestimo.usuario.nome
        titulo = emprestimo.livro.titulo
        editora = emprestimo.livro.editora
        generos = emprestimo.livro.generos
        autores = emprestimo.livro.autores
        data = datetime_para_str(emprestimo.data_emprestimo)
        identificador_exemplar = emprestimo.exemplar.identificacao


        print(f"""
                {bright_amarelo(LINHA_PONTILHADA)}
                {bright_amarelo('Empréstimo realizado com sucesso! \n')}
                {bright_amarelo('Nome do usuário: ')}{nome}
                {bright_amarelo('Título: ')}{titulo}
                {bright_amarelo('Editora: ')}{editora}
                {bright_amarelo('Autor(s): ')}{', '.join(autores)}
                {bright_amarelo('Gêneros: ')}{', '.join(generos)}
                {bright_amarelo('Data do empréstimo: ')}{data}
                {bright_amarelo('Número do exemplar: ')}{identificador_exemplar}
                {bright_amarelo(LINHA_PONTILHADA)}
        """)

    except ValueError as erro:
        print(bright_vermelho('\n\tNão foi possível realizar a operação de empréstimo.')) # pylint: disable=line-too-long
        # print(bright_vermelho(f'\n\t{str(erro)}'))
        print(str(erro))

###########################################################
                  # RENOVAR #
###########################################################
def renovar() -> None:
    '''
    Fluxo do renovar empréstimo
    '''
    try:
        usuario_nome = get_nome_usuario()
        livro_titulo = get_livro_titulo()
        numero_do_exemplar = input_int('\n\tEntre com o número do exemplar: ')

        renovar_emprestimo: Emprestimo = BIBLIOTECA.renovar_emprestimo(
            usuario_nome,
            livro_titulo,
            numero_do_exemplar
        )
        generos = renovar_emprestimo.livro.generos
        autores = renovar_emprestimo.livro.autores
        data = datetime_para_str(renovar_emprestimo.data_emprestimo)
        identificador_exemplar = renovar_emprestimo.exemplar.identificacao
        print(f"""
                {bright_amarelo(LINHA_PONTILHADA)}
                {bright_amarelo('Renovação do empréstimo realizada com sucesso!\n')}
                {bright_amarelo('Nome do usuário: ')}{renovar_emprestimo.usuario.nome}
                {bright_amarelo('Título: ')}{renovar_emprestimo.livro.titulo}
                {bright_amarelo('Editora: ')}{renovar_emprestimo.livro.editora}
                {bright_amarelo('Autor(s): ')}{', '.join(autores)}
                {bright_amarelo('Gêneros: ')}{', '.join(generos)}
                {bright_amarelo('Data da renovação do empréstimo: ')}{data}
                {bright_amarelo('Número do exemplar: ')}{identificador_exemplar}
                {bright_amarelo(LINHA_PONTILHADA)}
        """)
    except ValueError as erro:
        print(bright_vermelho('\n\tNão foi possível realizar a operação de renovação do empréstimo.')) # pylint: disable=line-too-long
        # print(bright_vermelho(f'\n\t{str(erro)}'))
        print(str(erro))

###########################################################
                  # DEVOLVER #
###########################################################
def devolver() -> None:
    '''
    Fluxo de devolver empréstimo.
    '''
    try:
        usuario_nome = get_nome_usuario()
        livro_titulo = get_livro_titulo()
        numero_do_exemplar = input_int('\n\tEntre com o número do exemplar: ')

        devolver_emprestimo: Emprestimo = BIBLIOTECA.devolver_emprestimo(
            usuario_nome,
            livro_titulo,
            numero_do_exemplar
        )

        generos = devolver_emprestimo.livro.generos
        autores = devolver_emprestimo.livro.autores
        data = datetime_para_str(devolver_emprestimo.data_devolucao)
        identificador_exemplar = devolver_emprestimo.exemplar.identificacao
        print(f"""
                {bright_amarelo(LINHA_PONTILHADA)}
                {bright_amarelo('Devolução do empréstimo realizada com sucesso!\n')}
                {bright_amarelo('Nome do usuário: ')}{devolver_emprestimo.usuario.nome}
                {bright_amarelo('Título: ')}{devolver_emprestimo.livro.titulo}
                {bright_amarelo('Editora: ')}{devolver_emprestimo.livro.editora}
                {bright_amarelo('Autor(s): ')}{', '.join(autores)}
                {bright_amarelo('Gêneros: ')}{', '.join(generos)}
                {bright_amarelo('Data da devolução do empréstimo: ')}{data}
                {bright_amarelo('Número do exemplar: ')}{identificador_exemplar}
                {bright_amarelo(LINHA_PONTILHADA)}
        """)
    except ValueError as erro:
        print(bright_vermelho('\n\tNão foi possível realizar a operação de devolução do empréstimo.')) # pylint: disable=line-too-long
        # print(bright_vermelho(f'\n\t{str(erro)}'))
        print(str(erro))


###########################################################
                  # GERENCIAMENTO #
###########################################################
def gerenciamento_biblioteca() -> None:
    '''
    Fluxo Principal do Programa.
    '''
    limpar_console()
    print(verde('\t*** Gerenciamento da Biblioteca ***\n '))
    while True:

        opcao = escolher_uma_opcao_do_menu_entrada(OPCOES)
        if opcao == 'E':
            emprestar()
        if opcao == 'D':
            devolver()
        if opcao == 'R':
            renovar()
        if opcao == "S":
            print('Sair')
            break
