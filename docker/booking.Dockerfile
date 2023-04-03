FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt 
RUN python -m pip install --no-cache-dir twilio
COPY ./booking.py .
CMD [ "python", "./booking.py" ]