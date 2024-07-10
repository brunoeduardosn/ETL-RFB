FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    gdb

# Atualiza pip, setuptools e wheel antes de instalar as dependências
RUN pip install --upgrade pip setuptools wheel

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install -r requirements.txt

# Copia todo o código do projeto para o contêiner
COPY . .

# Copia o arquivo start_services.sh para o contêiner
COPY start_services.sh /app/start_services.sh

# Define permissões de execução para o start_services.sh
RUN chmod +x /app/start_services.sh

# Executa o start_services.sh quando o contêiner for iniciado
CMD ["/app/start_services.sh"]
