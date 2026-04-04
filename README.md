# Hệ Thống Quản Lý Hoạt Động Khoa Học
**Khoa An Toàn Thông Tin (PTIT)**

Đây là một dự án Fullstack chuẩn mực (Backend API + Frontend SPA + Database) nhằm phục vụ quản lý, đăng ký và theo dõi tiến độ các Hợp đồng/Đề tài Nghiên cứu Khoa học của Giảng viên và Sinh viên, được đóng gói hoàn toàn trong môi trường Docker.

## Công nghệ sử dụng
- **Backend**: FastAPI (Python), SQLAlchemy (Async), Passlib (Bcrypt), JWT Auth.
- **Frontend**: React (Vite), React Router, Axios, Lucide Icons. Thiết kế giao diện theo phong cách Academic Light Theme sạch sẽ.
- **Database**: PostgreSQL 15, sử dụng engine `asyncpg` tối ưu luồng I/O bất đồng bộ.
- **DevOps**: Docker, Docker Compose, Multi-stage builds với Nginx phục vụ web tĩnh.

---

## Tính năng và Chức năng Chính của Hệ Thống

Hệ thống được thiết kế theo quy trình nghiệp vụ thực tế của khoa, bao gồm các module chức năng cốt lõi:

**1. Hệ thống Phân quyền Quản trị (Authentication & Authorization)**
- Đăng nhập bảo mật sử dụng **JWT (JSON Web Token)** với mật khẩu được băm bằng chuẩn `bcrypt`.
- Phân tách quyền hạn truy cập theo 3 cấp độ: `ADMIN`, `TEACHER` (Giảng viên) và `STUDENT` (Sinh viên). 
  *(Ví dụ: Sinh viên có thể xem Danh sách, nhưng chỉ Giảng viên và Admin mới có quyền khởi tạo Đề tài mới).*

**2. Quản lý Đề Tài Nghiên cứu Khoa học (Projects)**
- **Đăng ký mới**: Ghi nhận toàn bộ thông tin Đề tài (Tên đề tài, Lĩnh vực, Kinh phí dự kiến, Thời gian bắt đầu/kết thúc).
- **Theo dõi Trạng thái**: Số hóa các vòng đời của 1 đề tài bằng các nhãn trạng thái trực quan: `DRAFT` (Bản nháp) -> `SUBMITTED` (Chờ duyệt) -> `APPROVED` (Đang triển khai) -> `COMPLETED` (Hoàn thành) hoặc `REJECTED` (Bị từ chối).
- Hiển thị danh sách tổng quan trên màn hình Dashboard bằng giao diện bảng hiện đại.

**3. Quản lý Nhóm Nghiên cứu (Project Members)**
- Tự động gán quyền Chủ nhiệm Đề tài (`CHAIRMAN`) cho cá nhân khởi tạo.
- Hỗ trợ mô hình kết nối N-N: Có thể thêm/bớt nhiều nhân sự (`MEMBER`, `SECRETARY`) cùng tham gia đóng góp cho một đề tài.

**4. Quản lý Minh chứng Công bố Khoa học (Publications)**
- Nơi các Giảng viên/Sinh viên đăng tải và gắn kèm link các bài báo khoa học, kỉ yếu hội thảo (Tên bài, tên tạp chí, ngày publish). Các bài báo này có thể được gán/tham chiếu trực tiếp vào một Đề tài NCKH cụ thể làm minh chứng nghiệm thu trực tiếp.

---

Hệ thống đã được thiết kế sẵn **Seed Data** (dữ liệu mẫu) và luồng tự khởi tạo Database. Bạn không cần setup các môi trường Python hay Node.js rườm rà.

Điều kiện tiên quyết: Máy tính của bạn đã cài đặt sẵn **Docker** và **Docker Compose**.

1. Clone hoặc tải mã nguồn về.
2. Mở Terminal / Command Prompt tại thư mục gốc dự án (ngang hàng với file `docker-compose.yml`).
3. Chạy lệnh sau:
   ```bash
   docker-compose up -d --build
   ```
4. Đợi Docker tải Images và khởi chạy. Khi quá trình hoàn tất (các container hiển thị `Running` / `Healthy`), hệ thống đã sẵn sàng phục vụ.

---

## Cách Test Hệ Thống (MVP)

Sau khi hệ thống khởi chạy thành công, bạn kiểm tra 2 cổng dịch vụ sau:

### 1. Trải nghiệm giao diện Web (Frontend)
- Mở trình duyệt và truy cập: [http://localhost](http://localhost)
- Hệ thống bảo mật sẽ yêu cầu bạn đăng nhập. Vui lòng sử dụng tài khoản Seed Data đã được cắm sẵn vào DB:
  - **Tên đăng nhập:** `admin`
  - **Mật khẩu:** `admin123`
- Đăng nhập thành công, bạn sẽ thấy giao diện Dashboard lịch sự cùng nút mở tab **Tất cả Đề tài** đổ dữ liệu thời gian thực từ Postgres.

### 2. Trải nghiệm môi trường API (Backend)
- Để truy cập trang tài liệu Swagger UI của FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Tại đây bạn có thể thấy tất cả các luồng Endpoints (`/api/auth`, `/api/projects`).
- Để test thẳng trên Swagger: Bấm vào biểu tượng ổ khóa **[Authorize]** trên góc phải màn hình, điền `admin` và `admin123` để nhận JWT Token. Sau đó gọi thử Endpoint hiển thị Data tùy thích.

---

## Cách tắt Hệ thống
Để tắt và xóa dọn rác các container (Lưu ý: Dữ liệu DB đã được mount ra Volume ngoài nên **không** bị mất):
```bash
docker-compose down
```
