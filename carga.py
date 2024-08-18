'''
Módulo com fluxo principal de carga DB.
  
'''

from src.db.carga_db import carregar_banco_de_dados
from src.db.conexao_db import get_conexao_db

if __name__ == "__main__":
    carregar_banco_de_dados(get_conexao_db())
