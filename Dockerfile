FROM python-3.8

WORKDIR /app

COPY . /app

RUN cd /app
RUN export PIPENV

RUN pip install pipenv

CMD ["python3", "manage.py", "runserver"]
