FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Expose Vite's default port
EXPOSE 5173

# Run dev server with host 0.0.0.0 to accessible outside container
CMD ["npm", "run", "dev", "--", "--host"]
