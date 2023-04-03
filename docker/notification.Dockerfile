FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN pip3 install twilio
COPY ./notification.py .
CMD [ "python", "./notification.py" ]