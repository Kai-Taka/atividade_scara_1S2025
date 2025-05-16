FROM python:3.11.12-bookworm

#Instalar dependencias python
COPY requirements ./
RUN pip install --no-cache-dir -r requirements

COPY scara.py ./src/scara.py

CMD ["python", "./src/scara.py"]