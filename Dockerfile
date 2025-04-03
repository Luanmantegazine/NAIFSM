# Use an official Raspberry Pi 3 image as the base image
FROM node:10-alpine

#RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
#RUN python3 -m ensurepip
#RUN pip3 install --no-cache --upgrade pip setuptools

# Create the app directory in the container
WORKDIR /app

# Copy the HTML file to the app directory in the container
COPY hello.js .
#COPY helloworldp.py .

# Serve the HTML file using an HTTP server
CMD [ "node", "hello.js" ]
#CMD [ "python", "helloworldp.py" ]

EXPOSE 8080
