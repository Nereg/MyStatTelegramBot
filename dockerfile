FROM python:3

ADD ./ /main/

WORKDIR /main/
RUN pip install -r requirements.txt
RUN python /main/migration.py
WORKDIR /main/src/
RUN mkdir -p ../logs/
RUN touch ../logs/main.log

CMD [ "python", "/main/src/main.py" ]











