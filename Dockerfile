FROM python:3.7
RUN pip3 install telethon PySocks
COPY . TeleSaver
WORKDIR /TeleSaver
CMD ["python3", "./TeleSaver.py"]