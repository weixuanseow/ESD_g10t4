FROM python:3-slim
WORKDIR /usr/src/app
COPY ../requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./booktest.py ./invokes.py 
COPY ../msvc_booking/ booking.py
COPY ../msvc_patient/ patient.py
COPY ../msvc_notification/ notification.py
CMD [ "python", "./booktest.py" ]