# Hệ Thống Quản Lý Đề Tài Nghiên cứu Khoa học (NCKH)
**Dự án Bài Tập Lớn (BTL) - Tái cấu trúc đơn giản cho người mới bắt đầu**

Dự án là một hệ thống Website Full-Stack tối giản giúp quản lý vòng đời đề tài nghiên cứu khoa học, phân quyền rõ ràng giữa Admin, Giảng viên và Sinh viên.

## Công Nghệ Sử Dụng (Tối Giản)

- **Backend**: Python 3.10+, **Flask** (Framework siêu nhẹ), **psycopg2** (Viết câu lệnh SQL thuần túy - Raw SQL).
- **Cơ Sở Dữ Liệu**: **PostgreSQL** 15.
- **Frontend**: **Vanilla HTML, CSS, JavaScript** (Không dùng framework phức tạp, dễ đọc, dễ sửa).
- **Deployment**: **Docker** & **Docker Compose** (Chạy toàn bộ hệ thống chỉ với 1 câu lệnh).

---

## Cấu Trúc Thư Mục

```text
BTL-PY/
├── app/                # Backend Flask
│   ├── main.py         # Điểm khởi chạy chính
│   ├── auth.py         # Chức năng Đăng nhập
│   ├── projects.py     # Chức năng Quản lý Đề tài
│   ├── users.py        # Chức năng Admin quản lý người dùng
│   ├── db.py           # Kết nối Cơ sở dữ liệu
│   ├── Dockerfile      # Cấu hình Docker cho Flask
│   └── requirements.txt
├── frontend/           # Frontend Vanilla JS
│   ├── css/            # Giao diện (style.css)
│   ├── js/             # Logic xử lý (app.js)
│   ├── index.html      # Trang giới thiệu
│   ├── login.html      # Trang đăng nhập
│   ├── dashboard.html  # Trang chính (Dynamic theo Role)
│   └── Dockerfile      # Cấu hình Nginx để phục vụ file tĩnh
├── init.sql            # Tạo bảng và Dữ liệu mẫu (Seed Data)
└── docker-compose.yml  # File điều phối toàn bộ hệ thống
```

---

## Hướng Dẫn Khởi Chạy

Bạn cần cài đặt **Docker** và **Docker Desktop** trên máy tính.

1. **Mở Terminal/PowerShell** tại thư mục gốc của dự án.
2. **Chạy lệnh xây dựng và khởi động**:
   ```bash
   docker compose up --build -d
   ```
3. **Truy cập ứng dụng**:
   - Giao diện người dùng: [http://localhost](http://localhost)
   - API Backend (Nếu muốn test Postman): [http://localhost:8000](http://localhost:8000)

---

## Tài Khoản Thử Nghiệm

Hệ thống đã nạp sẵn các tài khoản sau để bạn kiểm tra các quyền (Role):

| Role | Username | Password | Chức năng chính |
| :--- | :--- | :--- | :--- |
| **ADMIN** | `admin` | `admin123` | Quản lý người dùng, Duyệt/Hủy đề tài toàn hệ thống. |
| **TEACHER** | `teacher1` | `123456` | Tạo đề tài, Duyệt sinh viên tham gia đề tài của mình. |
| **STUDENT** | `student1` | `123456` | Xem danh sách đề tài, Gửi yêu cầu tham gia. |

---

## Các Chức Năng Chính Theo Role

- **Admin**:
  - Xem thống kê và toàn bộ danh sách đề tài.
  - Thay đổi trạng thái đề tài (Duyệt/Hủy bỏ).
  - Quản lý tài khoản (Thêm/Xóa Giảng viên, Sinh viên).
- **Giảng viên (Teacher)**:
  - Thêm, sửa, xóa các đề tài do mình hướng dẫn.
  - Phê duyệt sinh viên gửi yêu cầu tham gia đề tài.
- **Sinh viên (Student)**:
  - Xem các đề tài nghiên cứu đang có.
  - Gửi yêu cầu tham gia đề tài cho giảng viên.
  - Xem trạng thái yêu cầu (Đã duyệt/Từ chối).
