FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
#amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt 
# -r amqp.reqs.txt
COPY ./dispense_restock.py ./invokes.py ./amqp_setup.py ./send_order.py ./
COPY ./patient.py .
COPY ./inventory.py .
CMD [ "python", "./dispense_restock.py" ]