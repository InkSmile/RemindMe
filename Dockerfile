FROM python-3.8

RUN apt-get update && apt-get install -y --no-install-recommends

WORKDIR /app

COPY . /app

RUN cd /app
RUN mkdir /static
RUN export PIPENV

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["./entrypoint.sh"]
