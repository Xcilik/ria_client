FROM python:3.8

WORKDIR /smal

RUN python3 -m pip install -U pip
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/
RUN pip3 install https://github.com/KurimuzonAkuma/pyrogram/archive/dev.zip --force-reinstall

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

CMD ["bash", "start"]
