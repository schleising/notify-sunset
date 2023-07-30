FROM python:3-slim
ENV PYTHONUNBUFFERED 1

# Install the build tools
RUN apt update && apt install -y git

# Make the code directory
RUN mkdir /code
WORKDIR /code

# Install requirements for the covid charts script
COPY . /code/
RUN pip install -r ./requirements.txt

# Run a command to ensure the container does not exit
CMD [ "python", "notify-sunset.py" ]
