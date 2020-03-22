FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /src
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install
ADD app.py /
ENTRYPOINT ["python3", "./gitlab_stats.py"]
