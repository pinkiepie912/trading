FROM python:3.9-buster

#
# Configure
#
ARG POETRY_VERSION=1.1.11
ARG ENV=production
ENV PROJECT_ROOT=/trading

ARG DEBIAN_FRONTEND=noninteractive
ARG TERM=linux
ARG POETRY_HOME=/opt/potry

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN echo ${ENV}

#
# Install System packages
#

#ARG DEBIAN_FRONTEND=noninteractive
#RUN apt-get update -y


#
# Setup Poetry
#

# install poetry - respects $POETRY_VERSION, $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Use docker environment instead of virtualenv
RUN poetry config virtualenvs.create false

# Copy install files
COPY ./app/trading/pyproject.toml ${PROJECT_ROOT}/app/trading/pyproject.toml
COPY ./app/trading/poetry.lock ${PROJECT_ROOT}/app/trading/poetry.lock
COPY ./lib/trading-db ${PROJECT_ROOT}/lib/trading-db
COPY ./lib/trading-strategy ${PROJECT_ROOT}/lib/trading-strategy

#
# Install Python packages
#
WORKDIR ${PROJECT_ROOT}/app/trading
RUN if [ ${ENV} != "production" ]; then \
        POETRY_ARGS=""; \
    else \
        POETRY_ARGS="--no-dev"; \
    fi; \
    poetry install \
        --no-interaction \
        --no-ansi \
        ${POETRY_ARGS}

#
# Copy sources
#
COPY ./app/trading ${PROJECT_ROOT}/app/trading

#
# Run commands
#

EXPOSE 8080
CMD uvicorn app:app --host 0.0.0.0 --port 8080
