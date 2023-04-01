FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt -r amqp.reqs.txt
COPY ./dispense_restock.py ./invokes.py ./amqp_setup.py ./send_order.py ./
CMD [ "python", "./dispense_restock.py" ]