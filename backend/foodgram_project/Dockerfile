FROM python:3.7-slim

WORKDIR /app

COPY backend/foodgram_project/requirements.txt .

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram_project.wsgi:application", "--bind", "0:9999" ]
