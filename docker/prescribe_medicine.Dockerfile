FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN pip3 install twilio
COPY ./invokes.py .
COPY ./prescribe_medicine.py .
COPY ./patient.py .
COPY ./prescription_check.py .
CMD [ "python", "./prescribe_medicine.py", "--host=0.0.0.0", "--port=5101"]