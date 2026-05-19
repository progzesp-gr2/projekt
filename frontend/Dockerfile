FROM node:26 AS build

WORKDIR /web
COPY . /web/

RUN npm install
RUN npm run build

FROM nginx:1.31

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /web/dist/ /usr/share/nginx/html
