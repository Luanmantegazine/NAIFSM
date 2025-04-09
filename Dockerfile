# Use a modern Node.js version
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy the file
COPY hello.js .

# Install dependencies or add more steps
# RUN npm install

CMD ["node", "hello.js"]

EXPOSE 8000
