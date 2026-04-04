import React, { useState, useEffect } from 'react';
import api from './api';
import { FileText, Clock, CheckCircle, XCircle, FilePlus, PlayCircle } from 'lucide-react';

function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/projects/');
      setProjects(response.data);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Lỗi khi tải danh sách đề tài. Vui lòng kiểm tra lại kết nối.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    switch(status) {
      case 'DRAFT': return <span className="status-badge status-draft"><FileText size={14}/> Bản nháp</span>;
      case 'SUBMITTED': return <span className="status-badge status-pending"><Clock size={14}/> Chờ duyệt</span>;
      case 'APPROVED': return <span className="status-badge status-approved"><PlayCircle size={14}/> Đang thực hiện</span>;
      case 'COMPLETED': return <span className="status-badge status-success"><CheckCircle size={14}/> Hoàn thành</span>;
      case 'REJECTED': return <span className="status-badge status-danger"><XCircle size={14}/> Bị từ chối</span>;
      default: return <span className="status-badge">{status}</span>;
    }
  }

  if (loading) return <div className="loading-spinner">Đang tải dữ liệu JSON...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="table-container">
      <div className="table-header">
        <h3>Danh Sách Đề Tài Nghiên Cứu</h3>
        <button className="btn-primary" style={{display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', borderRadius: '6px', border: 'none', background: '#3b82f6', color: '#fff', cursor: 'pointer'}}>
          <FilePlus size={18} /> Đăng ký đề tài
        </button>
      </div>
      
      {projects.length === 0 ? (
        <div className="empty-state">Hệ thống hiện tại chưa có đề tài nào.</div>
      ) : (
        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Tên đề tài</th>
                <th>Lĩnh vực</th>
                <th>Trưởng nhóm (ID)</th>
                <th>Năm</th>
                <th>Trạng thái</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.id}>
                  <td className="font-medium text-primary">{project.title}</td>
                  <td>{project.research_field}</td>
                  <td className="text-muted text-sm" title={project.leader_id}>
                    {/* Chúng ta hiển thị một phần ID tượng trưng làm mã giảng viên */}
                    {project.leader_id.split('-')[0].toUpperCase()}
                  </td>
                  <td>{new Date(project.start_date).getFullYear()}</td>
                  <td>{getStatusBadge(project.status)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ProjectList;
