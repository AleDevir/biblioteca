'''
modelo Editora
'''

from src.model.base import Base

class Editora(Base):
    '''
    classe Editora
    '''
    def __init__(
            self,
            nome: str,
            identificacao: int = 0,
        ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.nome: str = nome
