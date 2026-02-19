FROM python:3.14


WORKDIR /code


COPY ./dist/flexcity_app-0.1.0-py3-none-any.whl /code/flexcity_app-0.1.0-py3-none-any.whl

RUN pip install /code/flexcity_app-0.1.0-py3-none-any.whl

CMD ["fastapi", "run", "/usr/local/lib/python3.14/site-packages/flexcity_app/main.py", "--port", "80"]
#Debug image
#CMD ["tail", "-f", "/dev/null"]