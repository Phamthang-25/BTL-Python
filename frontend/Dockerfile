FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
# Copy cấu hình Nginx riêng để support React Router (tránh lỗi 404 khi f5 f5 trang reload)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Lấy các file build (ruột thư mục /dist) từ Stage 1 đem sang Image Nginx
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
