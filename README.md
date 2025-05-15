# UniFood
E-Commerce dedicado a Compra e Venda de Produtos Alimentícios na Faculdade - Unimar

## Estrutura Geral do Projeto

### 1. **UniFood/**
Diretório principal do projeto Django, contendo:
- **Configurações do projeto**: Arquivos como `settings.py`, `urls.py`, `wsgi.py` e `asgi.py` que configuram o funcionamento geral do projeto.
- **Gerenciamento de URLs**: O arquivo `urls.py` define as rotas principais e inclui as rotas do app `unifood_app`.

### 2. **unifood_app/**
Aplicação principal do projeto, responsável pelas funcionalidades específicas. Contém:
- **Modelos**: Diretório `models/` com as definições de dados, como o modelo `Usuario`.
- **Views**: Diretório `views/` com as funções que controlam o fluxo de dados e renderizam templates.
- **Templates**: Diretório `templates/` com os arquivos HTML para renderização das páginas.
- **Estáticos**: Diretório `static/` com arquivos CSS, JavaScript e outros recursos estáticos.
- **Rotas**: Arquivo `urls.py` que define as rotas específicas da aplicação.
- **Administração**: Arquivo `admin.py` para gerenciar os modelos no painel administrativo do Django.
- **Testes**: Diretório `tests/` com testes unitários para garantir a qualidade do código.

### 3. **Migrations**
O diretório `migrations/` dentro de `unifood_app/` contém os arquivos de migração do banco de dados, que registram as alterações feitas nos modelos.

### 4. **Outros Arquivos**
- **`manage.py`**: Script para gerenciar o projeto, como rodar o servidor e executar migrações.
- **`Pipfile`**: Gerencia as dependências do projeto, como Django e ferramentas de teste.
- **`Containerfile`**: Configuração para rodar o projeto em um container Docker.
- **`.gitignore`**: Define os arquivos e diretórios que devem ser ignorados pelo Git.

## Como Rodar o Projeto

1. Instale as dependências:
```bash
pipenv install
```

2. Ative o ambiente virtual:
```bash
pipenv shell
```

3. Aplique as migrações:
```bash
python manage.py migrate
```

4. Inicie o servidor:
```bash
python manage.py runserver
```

## Como Executar Testes do Projeto
Considerando a já instalação do ambiente de desenvolvimento, no terminal, você deverá executar o seguinte comando:

```bash
pipenv run cov
```

Assim, ele executará todos os testes criados dentro do diretório `tests/`. Caso deseja realizar o relatório desses testes, execute o comando:

```bash
pipenv run cov_report
```