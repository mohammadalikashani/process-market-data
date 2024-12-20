#######  Development #########
FROM python:3.11-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r ./requirements.txt
COPY manage.py .
COPY manage_rest.py .
COPY src ./src
# Rest Port
EXPOSE 8100