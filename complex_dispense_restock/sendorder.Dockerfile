FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./send_order.py ./amqp_setup.py ./ ./dispense_restock.py ./
CMD [ "python", "send_order.py" ]