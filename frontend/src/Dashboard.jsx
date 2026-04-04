import React, { useState, useEffect } from 'react';
import { LayoutDashboard, BookOpen, List, PlusCircle, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ProjectList from './ProjectList';

function Dashboard() {
  const [activeMenu, setActiveMenu] = useState('Tổng quan');
  const navigate = useNavigate();

  // Kiểm tra quyền truy cập lúc component vừa load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const menuItems = [
    { name: 'Tổng quan', icon: <LayoutDashboard size={20} /> },
    { name: 'Đề tài của tôi', icon: <BookOpen size={20} /> },
    { name: 'Tất cả Đề tài', icon: <List size={20} /> },
    { name: 'Đăng ký mới', icon: <PlusCircle size={20} /> },
  ];

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
              <div className="user-name">Người dùng Hệ thống</div>
              <div className="user-role">Đã thu thập Token</div>
            </div>
            <div className="avatar">U</div>
            <button className="btn-logout" title="Đăng xuất" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>

        <div className="content-area">
          {activeMenu === 'Tất cả Đề tài' ? (
            <ProjectList />
          ) : (
            <div className="dashboard-card" key={activeMenu}>
              <h3>Chào mừng đến với hệ thống NCKH</h3>
              <p>Trang này hiện đang hiển thị giao diện cho chức năng: <strong style={{ color: 'var(--primary-color)' }}>{activeMenu}</strong>.</p>
              <p style={{ marginTop: '20px' }}>Bạn đã đăng nhập thành công nhờ JWT Token.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
