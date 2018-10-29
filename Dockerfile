# Base image
FROM node:10.4.1-alpine

# Set working directory
RUN mkdir /usr/app
WORKDIR /usr/app

# Add `/usr/app/node_modules/.bin` to $PATH
ENV PATH /usr/app/node_modules/.bin:$PATH

# Install and cache app dependencies
# This way npm install only runs if package.json has changes
COPY package.json /usr/app/package.json
RUN npm install
RUN npm install react-scripts@1.1.1 -g

# Add application files
COPY ./public /usr/app/public
COPY ./src /usr/app/src

# Start app
CMD ["npm", "start"]
