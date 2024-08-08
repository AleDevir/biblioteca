'''
modelo Usuario
'''

from src.model.base import Base

class Usuario(Base):
    '''
    classe Usuario
    '''
    def __init__(
            self,
            nome: str,
            nacionalidade: str,
            telefone: str
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__()
        self.nome: str = nome
        self.nacionalidade: str = nacionalidade
        self.telefone: str = telefone
