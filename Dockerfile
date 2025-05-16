FROM silgi/silgiuserbot:silgiteam
RUN https://github.com/Hesenovhuseyn/LunaUserbot
WORKDIR /root/SilgiUserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
