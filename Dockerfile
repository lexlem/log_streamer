FROM python:2.7-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
ENV SECRET_KEY=x#gbyh0+nv9kb1o=h%h97m3lyev1-ycw99%f!=gfj@!qtpbg0^

# Supply your logs filename here
ENV LOG_FILE_PATH=./logs.jsonl

WORKDIR /log_streamer

CMD python manage.py runserver 0.0.0.0:8000