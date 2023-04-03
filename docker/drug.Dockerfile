FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./prescription_check.py ./openfda.py ./
CMD [ "python", "./prescription_check.py", "--host=0.0.0.0", "--port=5002"]