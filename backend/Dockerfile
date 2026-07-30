FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask" , "--app" , "wsgi" , "run" , "--host=0.0.0.0" , "--port=5000" , "--debug"]