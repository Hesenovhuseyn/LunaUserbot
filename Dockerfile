FROM python:3.11
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    ffmpeg \
    gcc \
    && apt-get clean
RUN pip install --upgrade pip
RUN pip install lxml
RUN pip install wheel
RUN pip install --upgrade pip setuptools
RUN apt-get update && apt-get install -y build-essential
RUN python3 --version
RUN git clone https://github.com/Hesenovhuseyn/LunaUserbot /root/LunaUserbot
WORKDIR /root/LunaUserbot/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
