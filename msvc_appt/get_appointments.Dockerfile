FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./get_appointments.py ./
CMD [ "python", "./get_appointments.py" ]