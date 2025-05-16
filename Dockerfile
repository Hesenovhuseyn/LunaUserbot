FROM silgi/silgiuserbot:silgiteam
RUN git clone https://github.com/Hesenovhuseyn/LunaUserbot /root/SilgiUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
