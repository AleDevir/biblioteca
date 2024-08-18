'''
modelo Livro
'''
from abc import abstractmethod
from src.model.base import Base
from src.model.autor import Autor
from src.model.exemplar import Exemplar
from src.model.genero import Genero

class Livro(Base):
    '''
    classe Livro
    '''
    def __init__(
            self,
            titulo: str,
            editora: str,
            generos: list[Genero],
            exemplares: list[Exemplar],
            autores: list[Autor],
            renovacoes_permitidas: int = 0,
            identificacao: int = 0
        ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.titulo: str = titulo
        self.editora: str = editora
        self.generos: list[Genero] = generos
        self.exemplares: list[Exemplar] = exemplares
        self.autores: list[Autor] = autores
        self.renovacoes_permitidas: int = renovacoes_permitidas

    @property
    def possui_exemplar_disponivel(self) -> bool:
        '''
        Informa se há exemplares disponíveis para o empréstimo.            
        '''
        return any(e.disponivel for e in self.exemplares)


    def retirar_exemplar(self) -> Exemplar:
        '''
        Retira um exemplar da lista de exemplares.
        Retorna o exemplar retirado.
        '''
        for exemplar in self.exemplares:
            if exemplar.disponivel:
                exemplar.emprestar()
                return exemplar
        raise ValueError ('\tNão existe exemplares disponíveis para o empréstimo.')

    def pode_ser_renovado(self) -> bool:
        '''
        Informa se o livro é renovável.
        '''
        return self.renovacoes_permitidas > 0


    def renovar_emprestimo_exemplar(self, exemplar: Exemplar) -> None:
        '''
        Renova o empréstimo do exemplar após as validações.
        '''
        if self.renovacoes_permitidas == 0:
            raise ValueError(f'\tO livro {self.titulo} não permite renovação.')

        if not exemplar.pode_renovar(self.renovacoes_permitidas):
            raise ValueError(f'\tNão é possível renovar o empréstimo do livro {self.titulo}. Você já atingiu o limite máximo de renovações permitidas.') # pylint: disable=line-too-long

        exemplar.acrescentar_numero_renovacoes()


    def devolver_exemplar(self, identificacao_exemplar: int) -> None:
        '''
        Devolve o exemplar emprestado para a lista de exemplares
        '''
        for exemplar in self.exemplares:
            if exemplar.identificacao == identificacao_exemplar:
                exemplar.devolver()
