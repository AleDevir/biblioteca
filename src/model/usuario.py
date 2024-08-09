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
            telefone: str,
            identificacao: int = 0
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.nome: str = nome
        self.nacionalidade: str = nacionalidade
        self.telefone: str = telefone
