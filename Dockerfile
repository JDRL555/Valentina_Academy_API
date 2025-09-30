FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instala tzdata y dependencias del sistema
RUN apt-get update && apt-get install -y \
    tzdata \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    libffi-dev \
    wget \
    wkhtmltopdf \
    libjpeg8 \
    libxrender1 \
    libfontconfig1 \
    xfonts-base \
    xfonts-75dpi \
    && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# Compila Python 3.13.5 desde fuente
WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/3.13.5/Python-3.13.5.tgz && \
    tar xzf Python-3.13.5.tgz && \
    cd Python-3.13.5 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    ln -s /usr/local/bin/python3.13 /usr/bin/python && \
    ln -s /usr/local/bin/pip3.13 /usr/bin/pip

# Crea directorio de trabajo
WORKDIR /app
COPY . /app

# Instala dependencias globalmente
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Da permisos al binario wkhtmltopdf
RUN chmod +x /usr/bin/wkhtmltopdf

# Comando de inicio
CMD python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8000