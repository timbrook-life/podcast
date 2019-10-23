FROM python:3.7

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src/ ./src
COPY ./twirp/ ./twirp
COPY ./conf/ ./conf
COPY ./entrypoint.sh ./entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "./entrypoint.sh" ]
