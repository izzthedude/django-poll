FROM python:3.10.5-alpine3.16

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /web

COPY ./requirements.txt /requirements.txt
COPY ./web /web

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home webapp && \
    chown -R webapp:webapp /web

ENV PATH="/venv/bin:$PATH"

USER webapp

RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]