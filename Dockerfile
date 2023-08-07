FROM python:3.8.16

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install vim \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

ARG NCP_SECRET_KEY
ENV NCP_SECRET_KEY=$NCP_SECRET_KEY

ARG NCP_ACCESS_KEY
ENV NCP_ACCESS_KEY=$NCP_ACCESS_KEY

ARG DEV_NAVER_CLLIENT_ID
ARG DEV_NAVER_REDIRECT_URI
ARG DEV_NAVER_CLIENT_SECRET

ARG DEV_KAKAO_CLLIENT_ID
ARG DEV_KAKAO_REDIRECT_URI

ENV DEV_NAVER_CLLIENT_ID=$DEV_NAVER_CLLIENT_ID
ENV DEV_NAVER_REDIRECT_URI=$DEV_NAVER_REDIRECT_URI
ENV DEV_NAVER_CLIENT_SECRET=$DEV_NAVER_CLIENT_SECRET

ENV DEV_KAKAO_CLLIENT_ID=$DEV_KAKAO_CLLIENT_ID
ENV DEV_KAKAO_REDIRECT_URI=$DEV_KAKAO_REDIRECT_URI

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
