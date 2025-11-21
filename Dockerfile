FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY ./api/* /app/
COPY ./cdi_generator.py /app/
COPY ./utils.py /app/
COPY ./api/requirements.txt /app/
COPY ./resources /app/resources

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"] 
