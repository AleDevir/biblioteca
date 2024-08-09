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
            identificacao: int = 0
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.nome: str = nome

    def __str__(self) -> str:
        '''
        retorna o nome.
        '''
        return self.nome
