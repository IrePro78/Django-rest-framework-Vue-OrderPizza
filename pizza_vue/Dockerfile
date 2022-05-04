#Base image
FROM node:16.13.2 as build

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

COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html