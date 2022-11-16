# syntax=docker/dockerfile:1.2

###########################
# Prepare build environment
###########################
FROM python:3.10-slim AS builder

RUN apt-get update && \
    apt-get install -y gcc ca-certificates wget curl git openssh-client

RUN mkdir /app
WORKDIR /app

# Set up poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy files required by Poetry for project installation
COPY pyproject.toml poetry.lock poetry.toml ./

# Add github.com as known SSH host
RUN mkdir -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

# Install production-only dependencies
RUN --mount=type=ssh --mount=type=cache,id=poetry,target=/root/.cache/pypoetry ~/.local/share/pypoetry/venv/bin/poetry install --no-dev --no-interaction

# Add source and start script
COPY src ./src

#############################
# Prepare runtime environment
#############################
FROM python:3.10-slim AS runtime

# These are required for Python 3 to behave correctly
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install necessary runtime dependencies
RUN apt-get update && \
    apt-get install gcc -y && \
    apt-get clean

# Create unprivileged user for running main process
RUN groupadd -g 999 nemobot && \
    useradd -m -r -u 999 -g nemobot nemobot
USER nemobot

# Copy source and virtualenv from builder
# The absolute path to our app root folder has to be
# exactly the same as used during installation.
# The reason behind this is that Poetry stores the
# absolute path in the `bin` folder of the virtual env.
COPY --chown=nemobot:nemobot --from=builder /app /app
WORKDIR /app

# Activate the virtualenv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH

CMD [ "python", "src/main.py" ]
