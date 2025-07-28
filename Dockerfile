FROM python:3.12-alpine

COPY src main.py ./

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 9005

CMD ["python3", "main.py", "--host=0.0.0.0" , "--port=9005"]