FROM ubuntu:22.04

# Evita prompts interactivos como el de tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Configura zona horaria por defecto
RUN apt-get update && apt-get install -y \
    tzdata \
    && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

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

# Crea entorno virtual
RUN python3 -m venv /app/venv

# Activa entorno virtual y instala dependencias
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Da permisos al binario wkhtmltopdf
RUN chmod +x /usr/bin/wkhtmltopdf

# Comando de inicio
CMD /app/venv/bin/python manage.py makemigrations && \
    /app/venv/bin/python manage.py migrate --noinput && \
    /app/venv/bin/python manage.py collectstatic --noinput && \
    /app/venv/bin/python manage.py runserver 0.0.0.0:8000