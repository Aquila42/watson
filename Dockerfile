FROM ubuntu:14.04
MAINTAINER Sai Karthik Reddy Ginni <saikarthik.reddy.ginni@columbia.edu>

RUN DEBIAN_FRONTEND=noninteractive apt-get update --fix-missing && apt-get install -y tar git curl nano wget dialog net-tools build-essential python python-dev python-distribute python-pip libfreetype6-dev libxft-dev libjpeg8-dev libpng12-dev libblas-dev liblapack-dev libatlas-base-dev gfortran libxslt-dev libxml2-dev

# Add code to watson folder
ADD . /watson

# change the working directory
WORKDIR /watson

# install requirements
RUN pip install -r requirements.txt

# download the nltk resources
RUN python -m nltk.downloader punkt stopwords

# expose port(s)
EXPOSE 80

CMD python main.py