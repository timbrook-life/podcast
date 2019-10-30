FROM python:3.8

ADD https://releases.hashicorp.com/consul-template/0.22.0/consul-template_0.22.0_linux_amd64.tgz ./consul-template.tgz
RUN tar -xzf ./consul-template.tgz
RUN rm ./consul-template.tgz

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src/ ./src
COPY ./twirp/ ./twirp
COPY ./conf/ ./conf

EXPOSE 5000

CMD ["./consul-template", "-log-level", "debug", "-config", "./conf/config.hcl"]
