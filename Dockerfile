FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN apt update -y
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod 777 entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]
