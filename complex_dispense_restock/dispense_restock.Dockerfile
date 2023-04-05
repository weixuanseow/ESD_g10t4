FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
#amqp.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
RUN apt-get update && apt-get install -y npm
RUN npm install -g vue
RUN npm install -g axios

COPY ./dispense_restock.py ./invokes.py ./amqp_setup.py ./
# COPY ../msvc_patient/patient.py  .
COPY send_order.py  .
# COPY ../msvc_inventory/inventory.py .
CMD [ "python", "./dispense_restock.py" ]