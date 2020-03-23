FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /src
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . .
ENTRYPOINT ["python", "./app.py"]
