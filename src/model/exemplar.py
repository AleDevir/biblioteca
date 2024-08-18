'''
modelo Exemplar
'''
from src.model.base import Base

class Exemplar(Base):
    '''
    classe Exemplar
    '''
    def __init__(
            self,
            identificacao: int,
            disponivel: bool = True,
            numero_de_renovacoes: int = 0,
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.disponivel: bool = disponivel
        self.numero_de_renovacoes: int = numero_de_renovacoes

    def emprestar(self) -> None:
        '''
        Emprestar
        '''
        if not self.disponivel:
            raise ValueError('Este exemplar já está emprestado!')
        self.disponivel = False

    def devolver(self) -> None:
        '''
        Devolver
        '''
        if self.disponivel:
            raise ValueError('Este exemplar não está emprestado!')
        self.disponivel = True

    def acrescentar_numero_renovacoes(self) -> None:
        '''
        Acrescenta +=1 na renovacao
        '''
        self.numero_de_renovacoes +=1

    def pode_renovar(self, renovacoes_permitidas: int) -> bool:
        '''
        Renova se puder.
        retorna False ou True
        '''
        if self.numero_de_renovacoes < renovacoes_permitidas:
            return True
        return False
