FROM node:22-bullseye

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm i

COPY . .

CMD [ "npm", "run", "dev" ]

# ! NEXT SETPS
# RUN docker compose exec nuxtapp npx prisma migrate dev
# RUN docker compose exec nuxtapp npx prisma generate
