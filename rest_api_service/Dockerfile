FROM python:3.7-slim-buster

ARG BUILD_ENV="local"

ENV APP_ENV=${BUILD_ENV}

# Setup system environment
# Set locales
ENV LANG=C.UTF-8
ENV LC_ALL C.UTF-8
# Enable python tracebacks on segfaults
ENV PYTHONFAULTHANDLER 1
# Stop generating .pyc files
#ENV PYTHONDONTWRITEBYTECODE 1
# Use random seed
ENV PYTHONHASHSEED random
# Enable unbuffered stdout/stderr stream
#ENV PYTHONUNBUFFERED 1
# Do not check whether a new version of pip is available
ENV PIP_DISABLE_PIP_VERSION_CHECK on
# Disable the cache
ENV PIP_NO_CACHE_DIR off
# Default timeout in seconds
ENV PIP_DEFAULT_TIMEOUT 100

ENV POETRY_VERSION 1.0.5

RUN echo "BUILD_ENV: ${BUILD_ENV}"

# Update the package list and Install the package required using noninteractive
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install nginx -y

# Install system dependencies
RUN pip install "poetry==${POETRY_VERSION}"

# Copy requirements
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/sites-enabled/default
COPY rest_api_service/nginx/default.conf /etc/nginx/sites-available/default
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Install application dependencies
RUN poetry config virtualenvs.create false \
	&& poetry install $(test "${BUILD_ENV}" = prod && echo "--no-dev") --no-interaction --no-ansi

# Install application into container
COPY . /app

# Cleanup package list
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Run the application
ENTRYPOINT ["python"]
CMD [ "-m", "rest_api_service.main"]
