# Use Node.js base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy dependency manifests
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Run the Vite development server
CMD ["npm", "run", "dev"]
