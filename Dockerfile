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
    xfonts-base \
    xfonts-75dpi \
    libjpeg8 \
    libxrender1 \
    libfontconfig1 \
    wkhtmltopdf \
    && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# Descarga y compila Python 3.13.5
WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/3.13.5/Python-3.13.5.tgz && \
    tar xzf Python-3.13.5.tgz && \
    cd Python-3.13.5 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall

# Crea directorio de trabajo
WORKDIR /app
COPY . /app

# Crea entorno virtual con Python 3.13.5
RUN python3.13 -m venv /app/venv

# Instala dependencias en el entorno virtual
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Da permisos al binario wkhtmltopdf
RUN chmod +x /usr/bin/wkhtmltopdf

# Comando de inicio
CMD /app/venv/bin/python manage.py makemigrations && \
    /app/venv/bin/python manage.py migrate --noinput && \
    /app/venv/bin/python manage.py collectstatic --noinput && \
    /app/venv/bin/python manage.py runserver 0.0.0.0:8000