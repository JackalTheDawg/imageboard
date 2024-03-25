FROM python:3.10

WORKDIR / social-network

RUN pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .