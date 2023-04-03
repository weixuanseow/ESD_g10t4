FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN pip3 install twilio
COPY ./booktest.py .
COPY ./invokes.py .
COPY ./booking.py .
COPY ./patient.py .
COPY ./notification.py .
CMD [ "python", "./booktest.py" ]