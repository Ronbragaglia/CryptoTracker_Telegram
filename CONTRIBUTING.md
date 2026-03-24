# Contribuindo para o Crypto Tracker Telegram

Obrigado por se interessar em contribuir com o Crypto Tracker Telegram! Este documento fornece diretrizes e instruções para contribuir com o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Documentação](#documentação)
- [Relatando Issues](#relatando-issues)
- [Pull Requests](#pull-requests)

## 🤝 Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e inclusivo. Por favor:

- Seja respeitoso com outros contribuidores
- Aceite e construa sobre feedback construtivo
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros da comunidade

## 🚀 Como Contribuir

### Maneiras de Contribuir

Existem várias maneiras de contribuir com o projeto:

1. **Reportar bugs** - Encontre e reporte problemas
2. **Sugerir melhorias** - Propor novas funcionalidades ou melhorias
3. **Enviar código** - Corrigir bugs ou implementar funcionalidades
4. **Melhorar documentação** - Ajudar a manter a documentação atualizada
5. **Revisar Pull Requests** - Ajudar a revisar o código de outros
6. **Responder questões** - Ajudar outros usuários com dúvidas

### Encontrando Issues para Trabalhar

Você pode encontrar issues abertas no [GitHub Issues](https://github.com/Ronbragaglia/CryptoTracker_Telegram/issues). Procure por issues com as labels:

- `good first issue` - Bom para iniciantes
- `help wanted` - Precisa de ajuda
- `enhancement` - Melhorias propostas
- `bug` - Bugs reportados

## 🔧 Processo de Desenvolvimento

### Configuração do Ambiente

1. **Fork o repositório**

```bash
# Fork no GitHub e clone seu fork
git clone https://github.com/SEU_USUARIO/CryptoTracker_Telegram.git
cd CryptoTracker_Telegram
```

2. **Configure o ambiente virtual**

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
pip install -e ".[dev]"
```

3. **Configure os pre-commit hooks**

```bash
pre-commit install
```

### Criando uma Branch

Crie uma branch para sua contribuição:

```bash
# Crie uma nova branch
git checkout -b feature/sua-feature

# Ou para correções de bugs
git checkout -b fix/seu-bug-fix
```

### Fazendo Mudanças

1. **Escreva código** seguindo os padrões do projeto
2. **Adicione testes** para cobrir suas mudanças
3. **Atualize a documentação** se necessário
4. **Execute os testes** para garantir que tudo funciona

```bash
# Execute os testes
pytest

# Execute com cobertura
pytest --cov=src/crypto_tracker --cov-report=html

# Execute os linters
black src/ tests/
flake8 src/ tests/ --max-line-length=100
mypy src/
```

### Commitando suas Mudanças

Use mensagens de commit claras e descritivas:

```bash
# Adicione suas mudanças
git add .

# Commit com mensagem clara
git commit -m "feat: adiciona suporte para nova exchange"

# Ou para correções
git commit -m "fix: corrige erro na extração de dados"
```

Siga o [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudanças na documentação
- `style:` formatação, ponto e vírgula, etc.
- `refactor:` refatoração de código
- `test:` adicionar ou corrigir testes
- `chore:` manutenção, atualização de dependências, etc.

## 📐 Padrões de Código

### Python

Seguimos os padrões PEP 8 e usamos as seguintes ferramentas:

- **Black** para formatação
- **Flake8** para verificação de estilo
- **MyPy** para verificação de tipos

```bash
# Formatar código
black src/ tests/

# Verificar estilo
flake8 src/ tests/ --max-line-length=100

# Verificar tipos
mypy src/ --strict
```

### Convenções de Nomenclatura

- **Classes**: `PascalCase` - `CryptoTracker`
- **Funções/Métodos**: `snake_case` - `collect_crypto_data`
- **Variáveis**: `snake_case` - `crypto_name`
- **Constantes**: `UPPER_SNAKE_CASE` - `MAX_CRYPTOS`
- **Módulos**: `snake_case` - `crypto_tracker`

### Documentação de Código

Use docstrings seguindo o estilo Google:

```python
def collect_crypto_data(self) -> List[Dict[str, Any]]:
    """
    Coleta dados de criptomoedas do CoinGecko.
    
    Returns:
        Lista de dicionários com dados das criptomoedas
        
    Raises:
        Exception: Se ocorrer erro durante a coleta
    """
    pass
```

## 🧪 Testes

### Escrevendo Testes

Escreva testes para novas funcionalidades e correções de bugs:

```python
import pytest
from crypto_tracker import CryptoTracker


def test_collect_crypto_data():
    """Testa coleta de dados de criptomoedas."""
    tracker = CryptoTracker()
    result = tracker.collect_crypto_data()
    assert isinstance(result, list)
```

### Executando Testes

```bash
# Execute todos os testes
pytest

# Execute testes específicos
pytest tests/test_tracker.py

# Execute com cobertura
pytest --cov=src/crypto_tracker --cov-report=html --cov-report=term-missing

# Execute em modo verbose
pytest -v
```

### Cobertura de Testes

Mantenha uma boa cobertura de testes:

```bash
# Verificar cobertura
pytest --cov=src/crypto_tracker --cov-report=term-missing
```

## 📚 Documentação

### Atualizando a Documentação

- Mantenha o README.md atualizado
- Adicione docstrings a novas funções/classes
- Atualize exemplos se necessário
- Adicione notas de release no CHANGELOG.md

### Estrutura da Documentação

```
docs/
├── index.md          # Documentação principal
├── installation.md   # Guia de instalação
├── usage.md          # Guia de uso
├── api.md            # Referência da API
└── contributing.md   # Guia de contribuição
```

## 🐛 Relatando Issues

### Antes de Reportar

1. **Verifique issues existentes** - Certifique-se de que o problema ainda não foi reportado
2. **Verifique a documentação** - O problema pode estar documentado
3. **Reproduza o problema** - Certifique-se de que pode reproduzir o problema

### Como Reportar

Ao criar uma issue, inclua:

1. **Título claro** - Descreva o problema de forma concisa
2. **Descrição detalhada** - Explique o problema em detalhes
3. **Passos para reproduzir** - Liste os passos para reproduzir o problema
4. **Comportamento esperado** - O que você esperava que acontecesse
5. **Comportamento atual** - O que realmente aconteceu
6. **Ambiente** - Versão do Python, sistema operacional, etc.
7. **Logs/Screenshots** - Inclua logs ou screenshots se relevantes

### Template de Issue

```markdown
## Descrição
Uma breve descrição do problema.

## Passos para Reproduzir
1. Passo 1
2. Passo 2
3. Passo 3

## Comportamento Esperado
O que você esperava que acontecesse.

## Comportamento Atual
O que realmente aconteceu.

## Ambiente
- Python: 3.11
- Sistema Operacional: Ubuntu 22.04
- Versão do Crypto Tracker: 2.0.0

## Logs/Screenshots
Inclua logs ou screenshots aqui.
```

## 🔄 Pull Requests

### Antes de Enviar

1. **Verifique se há issues relacionadas** - Referencie issues relacionadas no PR
2. **Atualize a documentação** - Inclua atualizações na documentação
3. **Adicione testes** - Certifique-se de que há testes para suas mudanças
4. **Execute os testes** - Certifique-se de que todos os testes passam
5. **Execute os linters** - Certifique-se de que o código segue os padrões

### Criando um Pull Request

1. **Fork e clone** o repositório
2. **Crie uma branch** para suas mudanças
3. **Faça suas mudanças** seguindo os padrões
4. **Commit suas mudanças** com mensagens claras
5. **Push para seu fork**
6. **Crie um Pull Request** no GitHub

### Título do Pull Request

Use um título claro e descritivo:

```
feat: adiciona suporte para nova exchange
fix: corrige erro na extração de dados
docs: atualiza README com novas instruções
```

### Descrição do Pull Request

Inclua na descrição:

- **Descrição das mudanças** - O que foi mudado e por que
- **Issues relacionadas** - Referencie issues relacionadas
- **Testes adicionados** - Descreva os testes adicionados
- **Documentação atualizada** - Liste a documentação atualizada
- **Screenshots** - Inclua screenshots se aplicável

### Revisão

Sua PR será revisada pelos mantenedores. Esteja preparado para:

- Responder a perguntas sobre suas mudanças
- Fazer ajustes baseados no feedback
- Adicionar mais testes se necessário
- Atualizar a documentação

### Mesclando

Após a aprovação, sua PR será mesclada na branch `main` ou `develop`.

## 🎉 Reconhecimento

Contribuidores serão reconhecidos no arquivo `CONTRIBUTORS.md` e nos releases do projeto.

## 📞 Contato

Se você tiver dúvidas sobre como contribuir:

- Abra uma issue no GitHub
- Entre em contato com os mantenedores
- Participe das discussões

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a Licença MIT.

---

Obrigado por contribuir com o Crypto Tracker Telegram! 🚀
