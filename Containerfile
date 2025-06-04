# Pegando imagem base
FROM python:3.12.0-alpine 

# Definindo diretório de trabalho
WORKDIR /app

# Instalando dependências
RUN python -m pip install pipenv
COPY Pipfile /app/
COPY Pipfile.lock /app/
RUN python -m pipenv install --system --deploy

# Copiando o restante do código
COPY . .

# Iniciando modelos de tabelas
RUN python manage.py migrate

# Expondo a porta do servidor
EXPOSE 8000

# Executando o servidor
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]