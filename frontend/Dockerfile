FROM node:20-alpine AS base
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .

FROM base AS build
RUN yarn build

FROM base AS test
RUN yarn test

FROM nginx:stable-alpine AS production

RUN apk add --no-cache apache2-utils
RUN htpasswd -bc /etc/nginx/.htpasswd dev sose2025

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
