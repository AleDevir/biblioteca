'''
modelo Livro
'''
from src.model.base import Base
from src.model.exemplar import Exemplar

class Livro(Base):
    '''
    classe Livro
    '''
    def __init__(
            self,
            titulo: str,
            editora: str,
            renovacoes_permitidas: int,
            generos: list[str],
            exemplares: list[Exemplar],
            autores: list[str]
        ) -> None:
        '''
        Inicialização
        '''
        super().__init__()
        self.titulo: str = titulo
        self.editora: str = editora
        self.renovacoes_permitidas: int = renovacoes_permitidas
        self.generos: list[str] = generos
        self.exemplares: list[Exemplar] = exemplares
        self.autores: list[str] = autores

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

    def renovar_emprestimo_exemplar(self, exemplar: Exemplar) -> None:
        '''
        Renova o empréstimo do exemplar após as validações.
        '''
        if self.renovacoes_permitidas == 0:
            raise ValueError(f'\tNão é possível renovar o empréstimo do livro {self.titulo}. Este livro não possui renovação.') # pylint: disable=line-too-long

        if not exemplar.pode_renovar(self.renovacoes_permitidas):
            raise ValueError(f'\tNão é possível renovar o empréstimo do livro {self.titulo}. Você já atingiu o limite máximo de renovações permitidas.') # pylint: disable=line-too-long

        exemplar.acrescentar_numero_renovacoes()

    def devolver_exemplar(self, id_exemplar: int) -> None:
        '''
        Devolve o exemplar emprestado para a lista de exemplares
        '''
        self.exemplares.append(Exemplar(id_exemplar))
