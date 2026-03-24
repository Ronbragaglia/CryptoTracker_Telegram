"""
Ponto de entrada para execução do pacote como módulo.

Permite executar o rastreador com: python -m crypto_tracker
"""

from .cli import main
import sys

if __name__ == '__main__':
    sys.exit(main())
