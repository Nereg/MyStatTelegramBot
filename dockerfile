FROM python:3

WORKDIR /

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
#migrate
RUN python migration.py


CMD [ "python", "./main.py" ]