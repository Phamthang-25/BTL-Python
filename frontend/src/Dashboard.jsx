import React, { useState, useEffect } from 'react';
import { LayoutDashboard, BookOpen, List, PlusCircle, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ProjectList from './ProjectList';
import MyProjects from './MyProjects';
import api from './api';

function Dashboard() {
  const [activeMenu, setActiveMenu] = useState('Tổng quan');
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // Kiểm tra quyền truy cập lúc component vừa load và fetch thông tin user
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    } else {
      fetchUser();
    }
  }, [navigate]);

  const fetchUser = async () => {
    try {
      const response = await api.get('/api/auth/me');
      setUser(response.data);
    } catch (err) {
      console.error('Không thể lấy thông tin user. Token lỗi?', err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  let menuItems = [
    { name: 'Tổng quan', icon: <LayoutDashboard size={20} /> },
    { name: 'Tất cả Đề tài', icon: <List size={20} /> }
  ];

  if (user && user.role !== 'STUDENT') {
    // Chèn vào giữa để thứ tự tự nhiên hơn
    menuItems.splice(1, 0, { name: 'Đề tài của tôi', icon: <BookOpen size={20} /> });
    menuItems.push({ name: 'Đăng ký mới', icon: <PlusCircle size={20} /> });
  }

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="avatar" style={{ width: 32, height: 32, fontSize: 14 }}>AT</div>
          <h2>Khoa ATTT</h2>
        </div>
        <nav className="nav-menu">
          {menuItems.map((item) => (
            <div
              key={item.name}
              className={`nav-item ${activeMenu === item.name ? 'active' : ''}`}
              onClick={() => setActiveMenu(item.name)}
            >
              {item.icon}
              <span>{item.name}</span>
            </div>
          ))}
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <header className="topbar">
          <div className="page-title">{activeMenu}</div>
          <div className="user-profile">
            <div className="user-info">
              <div className="user-name">{user ? user.username : 'GUEST'}</div>
              <div className="user-role">{user ? user.role : 'Đang tải...'}</div>
            </div>
            <div className="avatar">{user ? user.username.charAt(0).toUpperCase() : 'U'}</div>
            <button className="btn-logout" title="Đăng xuất" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>

        <div className="content-area">
          {activeMenu === 'Tất cả Đề tài' ? (
            <ProjectList user={user} />
          ) : activeMenu === 'Đề tài của tôi' ? (
            <MyProjects user={user} />
          ) : (
            <div className="dashboard-card" key={activeMenu}>
              <h3>Chào mừng đến với hệ thống NCKH</h3>
              <p>Trang này hiện đang hiển thị giao diện cho chức năng: <strong style={{ color: 'var(--primary-color)' }}>{activeMenu}</strong>.</p>
              <p style={{ marginTop: '20px' }}>
                {user 
                  ? `Xin chào ${user.role}! Bạn đã đăng nhập thành công nhờ JWT Token.` 
                  : 'Đang kết nối nhận diện...'}
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
