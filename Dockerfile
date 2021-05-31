FROM python:3.7

WORKDIR /app

COPY bfipricecrawler .

RUN pip install -r requirements.txt

EXPOSE 8000

RUN chmod +x /app/main.py

CMD ["python3", "main.py"]
