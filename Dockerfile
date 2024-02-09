# Use Python 3.8.6 slim image as base
FROM python:3.8.6-slim

# Install Graphviz and other dependencies
RUN apt-get update \
    && apt-get install -y graphviz \
    && rm -rf /var/lib/apt/lists/*

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

#
#
CMD ["uvicorn", "app.main:app" ,"--reload", "--host", "0.0.0.0", "--port", "50000"]