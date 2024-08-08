'''
modelo Biblioteca
'''
from src.model.base import Base
from src.model.emprestimo import Emprestimo, EMPRESTADO
from src.model.usuario import Usuario
from src.model.livro import Livro
from src.model.exemplar import Exemplar

class Biblioteca(Base):
    '''
    classe Biblioteca
    '''
    def __init__(
            self,
            usuarios: list[Usuario],
            livros: list[Livro],
            emprestimos: list[Emprestimo] = None
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__()
        self.usuarios: list[Usuario] = usuarios
        self.livros: list[Livro] = livros
        self.emprestimos: list[Emprestimo] = []
        if emprestimos:
            self.emprestimos = emprestimos

    def get_usuario_por_nome(self, nome_usuario: str) -> Usuario:
        '''
        Obtem o usuário por nome.
        Retorna o usuário.
        '''
        usuarios = [u for u in self.usuarios if u.nome.lower() == nome_usuario.lower()]
        if not usuarios:
            raise ValueError(f'O usuário |{nome_usuario}| não possui cadastro na Biblioteca.')

        return usuarios[0]

    def get_livro_por_titulo(self, titulo_livro: str) -> Livro:
        '''
        Obtem o livro por título.
        Retorna o livro.
        '''
        livros = [l for l in self.livros if l.titulo.lower() == titulo_livro.lower()]
        if not livros:
            raise ValueError(f'O livro |{titulo_livro}| não faz parte do acervo da Biblioteca.')

        return livros[0]

    def realizar_emprestimo(self, nome_usuario: str, titulo_livro: str) -> Emprestimo:
        '''
        Empresta ao usuario de nome o livro de título.
        Retorna o empréstimo.
        '''
        usuario: Usuario = self.get_usuario_por_nome(nome_usuario)
        livro: Livro = self.get_livro_por_titulo(titulo_livro)

        if not livro.possui_exemplar_disponivel:
            raise ValueError(f'O livro {livro.titulo} não possui exemplares disponíveis para empréstimo.') # pylint: disable=line-too-long

        exemplar: Exemplar = livro.retirar_exemplar()

        emprestimo: Emprestimo = Emprestimo(usuario, livro, exemplar) 
        self.emprestimos.append(emprestimo)
        return emprestimo

    def get_emprestimo_realizado(
        self,
        usuario: Usuario,
        livro: Livro,
        identificacao_exemplar: int
    ) -> Emprestimo:
        '''
        Obtem o emprestimo  realizado. 
        Retorna o emprestimo.
        '''
        for emprestimo in self.emprestimos:
            if (
                emprestimo.usuario == usuario
                and
                emprestimo.livro == livro
                and
                emprestimo.exemplar.identificacao == identificacao_exemplar
                and
                emprestimo.estado == EMPRESTADO
            ):
                return emprestimo
        raise ValueError(f"O emprestimo do usuário {usuario.nome} do livro {livro.titulo} não foi encontrado para o exemplar {identificacao_exemplar}.") # pylint: disable=line-too-long

    def devolver_emprestimo(
            self,
            nome_usuario: str,
            titulo_livro: str,
            identificacao_exemplar: int
    ) -> Emprestimo:
        '''
        Devolve a biblioteca o livro (identificação do exemplar) de título 
        emprestado para o usuário de nome.
        Retorna o Emprestimo.
        '''
        usuario: Usuario = self.get_usuario_por_nome(nome_usuario)
        livro: Livro = self.get_livro_por_titulo(titulo_livro)
        emprestimo: Emprestimo = self.get_emprestimo_realizado(
            usuario,
            livro,
            identificacao_exemplar
        )
        emprestimo.devolver()
        return emprestimo

    def renovar_emprestimo(
            self,
            nome_usuario: str,
            titulo_livro: str,
            identificacao_exemplar: int
    ) -> Emprestimo:
        '''
        Renova o emprestimo do livro (identificacao do exemplar) 
        de título emprestado para o usuário de nome.
        '''
        usuario: Usuario = self.get_usuario_por_nome(nome_usuario)
        livro: Livro = self.get_livro_por_titulo(titulo_livro)
        emprestimo = self.get_emprestimo_realizado(usuario, livro, identificacao_exemplar)
        emprestimo.renovar()
        return emprestimo
