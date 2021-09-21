FROM python:3.8

RUN mkdir /app
RUN mkdir /.streamlit
RUN mkdir /app/cfg
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app

RUN mkdir ~/.streamlit
RUN cp .streamlit/config.toml ~/.streamlit/config.toml
RUN cp .streamlit/credentials.toml ~/.streamlit/credentials.toml

RUN rm -rf tmp
EXPOSE 5000

ENTRYPOINT ["streamlit", "run"]

CMD ["main.py"]