# Use the official Nginx image based on Alpine Linux for a lightweight image.
FROM nginx:1.27.4-alpine-slim

# Copy all files from the current directory to the Nginx HTML folder.
COPY . /usr/share/nginx/html

# Expose port 80 to allow traffic.
EXPOSE 80
