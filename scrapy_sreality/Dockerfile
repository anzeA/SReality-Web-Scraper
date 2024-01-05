FROM python:3.9
WORKDIR /scrapy_sreality

RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN playwright install
COPY scrapy.cfg scrapy.cfg
COPY scrapy_sreality scrapy_sreality

CMD ["scrapy", "crawl", "sreality"]

#docker run -it my_scrape_image /bin/bash