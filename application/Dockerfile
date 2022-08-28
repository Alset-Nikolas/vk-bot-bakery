FROM python:3.9

WORKDIR /application
COPY requirements.txt /application
RUN pip install --upgrade pip &&  python -m pip install -r requirements.txt

COPY application /application
ENTRYPOINT ['python', 'main.py']