FROM python:3.8

WORKDIR /my_app

COPY . /my_app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python","data_streamer.py"]