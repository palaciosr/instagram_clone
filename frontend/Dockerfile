# FINAL WORKING VERSION – copy-paste this exactly
FROM node:20-alpine

# Optional: install serve only once (faster builds)
RUN npm install -g serve

WORKDIR /app

# Copy your built static files (dist, build, out, etc.)
COPY . .

EXPOSE 3000

# This will always work
CMD ["serve", "-s", ".", "-l", "3000"]