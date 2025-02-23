# Указываем версию пайтона
ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

# настройки окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFRED 1 

# создаем рабочию директорию 
RUN mkdir -p /code
WORKDIR /code

# копируем фаил зависемостей и устанавливаем их
COPY requirements.txt /tmp/reqirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
    
# копируем все файлы проэкта
COPY . /code

# копируем entrypoint скрипт и делаем его исполняемым
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# настройки окружения для Django
ENW SECRET_KEY "свой клучь от джанго"
# создание суперюзера параметры
ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_PASSWORD 1234
ENV DJANGO_SUPERUSER_EMAIL admin@gmail.com

# открываем порт 8000
EXPOSE 8000

# используем entrypoint скрипт
ENTRYPOINT ["/code/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]