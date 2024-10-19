FROM node:22

WORKDIR /app

COPY . .

RUN npm i

EXPOSE 3000

CMD [ "npm", "run", "dev" ]

# ! NEXT SETPS
# RUN docker compose exec nuxtapp npx prisma migrate dev
# RUN docker compose exec nuxtapp npx prisma generate
