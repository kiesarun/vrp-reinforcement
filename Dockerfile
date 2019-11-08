FROM python:3.6.8-jessie

RUN pip install scikit-learn 
RUN pip install matplotlib
RUN pip install numpy
RUN pip install flask
RUN pip install pymongo
RUN pip install python-dotenv
RUN pip install mlrose

RUN mkdir /app

WORKDIR /app

COPY . /app

CMD python app.py 