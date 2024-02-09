# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

WORKDIR /code
# 
CMD ["python3", "-m", "uvicorn", "app.main:app" ,"--reload", "--host", "0.0.0.0", "--port", "50000"]

# CMD ["uvicorn", "app.main:app" ,"--reload", "--host", "0.0.0.0", "--port", "50000"]