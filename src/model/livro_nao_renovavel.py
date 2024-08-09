'''
modelo Livro
'''
from src.model.livro import Livro
from src.model.exemplar import Exemplar

class LivroNaoRenovavel(Livro):
    '''
    classe Livro não renovável
    '''
    def pode_ser_renovado(self) -> bool:
        '''
        Informa se o livro é renovável.
        '''
        return False

    def renovar_emprestimo_exemplar(self, exemplar: Exemplar) -> None:
        '''
        Renova o empréstimo do exemplar após as validações.
        '''
        raise ValueError('\tNão é permitida renovação para este livro!')
