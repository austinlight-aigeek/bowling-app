# Dockerfile for frontend
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and lock file separately to leverage Docker cache
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the app
COPY . .

# Expose the port (optional if you don't rely on `docker-compose` for that)
EXPOSE 3000

# Run the React app
CMD ["npm", "start"]
