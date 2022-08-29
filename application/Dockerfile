FROM python:3.9

RUN mkdir /application
COPY . /application/
WORKDIR /application
RUN pip install --upgrade pip &&  python -m pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]