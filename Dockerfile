FROM ubuntu:22.04

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wkhtmltopdf \
    libjpeg8 \
    libxrender1 \
    libfontconfig1 \
    xfonts-base \
    xfonts-75dpi \
    && apt-get clean

# Crea directorio de trabajo
WORKDIR /app

# Copia tu proyecto
COPY . /app

# Instala dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Comando de inicio
CMD python manage.py makemigrations && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    chmod +x /usr/bin/wkhtmltopdf && \
    python manage.py runserver 0.0.0.0:8000