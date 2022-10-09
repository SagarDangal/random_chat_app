FROM python:3

# set working directory
WORKDIR /code

# copy all install dependencies
COPY /requirements.txt /requirements.txt
RUN pip3 install wheel
RUN pip3 install -r /requirements.txt

# copy app in code folder
COPY . ./

EXPOSE 8080

# run python api
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]