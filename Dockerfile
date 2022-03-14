FROM python:3.8-alpine

COPY . .

CMD ["python", "code/lab1.py"]