FROM node:22-bullseye

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm i --omit=dev

COPY . .

CMD ["tail", "-f", "/dev/null" ]

# ! NEXT SETPS
# RUN docker compose exec nuxtapp npx prisma migrate dev
# RUN docker compose exec nuxtapp npx prisma generate

# Should change the port in the package.json but seems to work without doing it
# RUN docker compose exec nuxtapp npm run dev

# docker ps
# docker inspect <ID> | grep "IPAddress"
# The try to insert it in nuxtapp???
