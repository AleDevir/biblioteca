## Biblioteca
<img src="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmlibGlvdGVjYXxlbnwwfHwwfHx8MA%3D%3D" alt="biblioteca" width="200px"/>


### Links Úteis:
+ [![Python](https://img.shields.io/badge/Python-blue)](https://www.python.org/downloads/)
+ [![Pylint](https://img.shields.io/badge/Pylint-yellowgreen)](https://pypi.org/project/pylint/)
+ [![Mypy](https://img.shields.io/badge/Mypy-darkblue)](https://mypy.readthedocs.io/en/stable/)
+ [![Pytest](https://img.shields.io/badge/Pytest-orange)](https://pypi.org/project/pytest/)


Comando para instalação dos pacotes:
```
pip install -r requirements.txt 

```
Verificação Estática de Código (pylint e mypy):
Para testar todos:

```
pylint *

# Para testar cada arquivo:
pylint <nome_do_arquivo.py> util

# Para testar um ou mais arquivos
mypy --show-error-codes --check-untyped-defs <nome_do_arquivo.py>  <nome_da_pasta>
