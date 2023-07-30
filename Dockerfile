FROM python:3-alpine as build
ENV PYTHONUNBUFFERED 1

# Install the build tools
RUN apk update && apk add git build-base

# Add the required packages, disabling cache to reduce the size of the image
COPY ./requirements.txt /requirements.txt
RUN pip install --user --no-cache-dir -r /requirements.txt

# Start witha fresh image after installing the necessary Python packages
FROM python:3-alpine

# Copy the python packages only from the build stage
COPY --from=build /root/.local /root/.local

# Make sure scripts in .local are in the PATH
ENV PATH=/root/.local/bin:$PATH

# Make the code directory
RUN mkdir /code
WORKDIR /code

# Install requirements for the covid charts script
COPY . /code/

# Run a command to ensure the container does not exit
CMD [ "python", "notify-sunset.py" ]
