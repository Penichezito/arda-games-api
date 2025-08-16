FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação

COPY . .    
# Expondo a porta que a API irá rodar
EXPOSE 8000

# Comando para rodar a API
# Uvicorn é o servidor ASGI que roda o FastAPI
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]