# Pegando imagem base
FROM python:3.12.0-alpine 

# Definindo diretório de trabalho
WORKDIR /app

# Instalando dependências
RUN python -m pip install pipenv
COPY Pipfile [Pipfile.lock](http://_vscodecontentref_/4) /app/
RUN python -m pipenv install --system --deploy

# Copiando o restante do código
COPY . .

# Criando usuário não-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Expondo a porta do servidor
EXPOSE 8000

# Executando o servidor
ENTRYPOINT [ "python", "manage.py", "runserver" ]