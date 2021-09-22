FROM python:3.8

RUN mkdir /app
RUN mkdir /.streamlit
RUN mkdir /app/cfg
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app

RUN rm -rf tmp
EXPOSE 5000

CMD streamlit run --server.port 5000 main.py