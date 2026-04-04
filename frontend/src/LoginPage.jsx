import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';
import { Lock, User } from 'lucide-react';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      // Vì FastAPI OAuth2PasswordRequestForm yêu cầu form-urlencoded data thay vì chuỗi JSON tĩnh
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/api/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      // Đăng nhập thành công, lưu token và đẩy sang màn hình chính
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        navigate('/dashboard'); 
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Đăng nhập thất bại. Kiểm tra lại thông tin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h2>Đăng Nhập</h2>
          <p>Hệ thống Quản lý NCKH - Khoa ATTT</p>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <User className="input-icon" size={18} />
            <input 
              type="text" 
              placeholder="Tên đăng nhập" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required 
            />
          </div>
          <div className="input-group">
            <Lock className="input-icon" size={18} />
            <input 
              type="password" 
              placeholder="Mật khẩu" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required 
            />
          </div>
          <button disabled={loading} type="submit" className="btn-login">
             {loading ? 'Đang xử lý...' : 'Đăng Nhập'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
