#Base image
FROM node:16.13.2 as builder

#Install serve package
RUN npm i -g serve

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Copy the project files
COPY . ./

# Build the project
RUN npm run build

# Server http
FROM nginx:1.21.6

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/* \

RUN rm -rf /usr/share/nginx/html/*

RUN mkdir /usr/share/nginx/logs

RUN rm -rf /etc/nginx/conf.d/default.conf

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

##Install serve package
#RUN npm i -g serve
#
## Set the working directory
#WORKDIR /app
#
## Copy the package.json and package-lock.json
#COPY package*.json ./
#
## install project dependencies
#RUN npm install
#
## Copy the project files
#COPY . ./
#
## Build the project
##RUN npm run build
#
## Expose a port
##EXPOSE 8000
#
## Executables
##CMD [ "serve", "-s", "dist" ]
#CMD [ "npm", "run", "serve" ]