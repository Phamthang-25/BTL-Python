# Sử dụng base image là python:3.11-slim để giảm dung lượng
FROM python:3.11-slim

# Thiết lập Environment Variables
# PYTHONDONTWRITEBYTECODE: Ngăn Python ghi các file compile bytecode (.pyc) ra đĩa.
# PYTHONUNBUFFERED: Ngăn Python buffer output (stdout/stderr), giúp log hiển thị ngay lập tức ra terminal.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy danh sách thư viện vào trước để docker cache lại (giảm thời gian build lại nếu mã nguồn thay đổi mà requirements vẫn không thay đổi)
COPY requirements.txt .

# Cài đặt thư viện bằng list trên 
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn (.env, app/, v.v.) vào thư mục làm việc /app trong container
COPY . .

# Mở cổng 8000 để map ra ngoài (Bước khai báo, có giá trị documentation)
EXPOSE 8000

# Khởi chạy server uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
