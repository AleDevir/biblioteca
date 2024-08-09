'''
modelo Genero
'''

from src.model.base import Base

class Genero(Base):
    '''
    classe Genero
    '''
    def __init__(
            self,
            nome: str,
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__()
        self.nome: str = nome

    def __str__(self) -> str:
        '''
        retorna o nome.
        '''
        return self.nome
