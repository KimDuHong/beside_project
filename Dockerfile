FROM python:3.8.16

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install vim \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

RUN mkdir /beside_project
COPY . /beside_project/
WORKDIR /beside_project
COPY poetry.lock pyproject.toml /beside_project/

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt
# RUN poetry config virtualenvs.create false
# RUN poetry install --no-interaction --no-ansi
