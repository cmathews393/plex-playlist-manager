FROM python:latest

ENV SRC_DIR /usr/bin/ppm/
COPY . ${SRC_DIR}/
WORKDIR ${SRC_DIR}

ENV PYTHONUNBUFFERED=1
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "plexplaylistmanager/__init__.py"]