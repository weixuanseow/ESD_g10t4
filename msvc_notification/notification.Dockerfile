FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install twilio
COPY ./notification.py ./
CMD [ "python", "./notification.py" ]