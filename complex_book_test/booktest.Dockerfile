FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install twilio
COPY ./booktest.py .
COPY invokes.py .
# COPY ../msvc_booking/booking.py .
# COPY ../msvc_patient/patient.py .
# COPY ../msvc_notification/notification.py .
CMD [ "python", "./booktest.py" ]