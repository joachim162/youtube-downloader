# Base image
FROM python:latest

WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy src files
COPY ./src /app/

# Run app
ENTRYPOINT [ "python", "__init__.py" ]

