FROM python:3.9

WORKDIR /code

COPY ./pip-requirements.txt /code/pip-requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/pip-requirements.txt

COPY ./ingestor/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ingestor/app /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]
