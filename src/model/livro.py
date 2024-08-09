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
        ) -> None:
        '''
        Inicialização
        '''
        super().__init__()
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
        if len(self.exemplares) > 0:
            return True
        return False

    def retirar_exemplar(self) -> Exemplar:
        '''
        Retira um exemplar da lista de exemplares.
        Retorna o exemplar retirado.
        '''
        if not self.exemplares:
            raise ValueError ('\tNão existe exemplares disponíveis para o emrestimo.')
        return self.exemplares.pop()


    @abstractmethod
    def pode_ser_renovado(self) -> bool:
        '''
        Informa se o livro é renovável.
        '''

    @abstractmethod
    def renovar_emprestimo_exemplar(self, exemplar: Exemplar) -> None:
        '''
        Renova o empréstimo do exemplar após as validações.
        '''


    def devolver_exemplar(self, id_exemplar: int) -> None:
        '''
        Devolve o exemplar emprestado para a lista de exemplares
        '''
        self.exemplares.append(Exemplar(id_exemplar))
