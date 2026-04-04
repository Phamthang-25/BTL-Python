import axios from 'axios';

// Khởi tạo một đối tượng axios với cấu hình mặc định
const api = axios.create({
  baseURL: 'http://localhost:8000',
  // timeout can be set here if needed
});

// Thêm Interceptor: Can thiệp vào MỌI request gửi đi
api.interceptors.request.use(
  (config) => {
    // 1. Tìm token trong localStorage
    const token = localStorage.getItem('token');
    
    // 2. Nếu có, đính kèm vào phần Header chuẩn HTTP Bearer
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor cho Response (Tùy chọn: Xử lý nếu token hết hạn)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Tự động logout nếu token không đổi hoặc quá hạn
            localStorage.removeItem('token');
            // Cần cẩn thận khi sử dụng window.location, tốt nhất nên quản lý qua React Context
            window.location.href = '/login'; 
        }
        return Promise.reject(error);
    }
);

export default api;
