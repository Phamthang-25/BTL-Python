import React, { useState, useEffect } from 'react';
import api from './api';
import { FileText, Clock, CheckCircle, XCircle, FilePlus, PlayCircle, Trash2, Eye } from 'lucide-react';

function ProjectList({ user }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Create Modal states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newProject, setNewProject] = useState({ title: '', research_field: '', start_date: '' });
  const [submitting, setSubmitting] = useState(false);

  // Read-only Details Modal states
  const [viewProject, setViewProject] = useState(null);
  const [viewMembers, setViewMembers] = useState([]);
  const [viewPubs, setViewPubs] = useState([]);

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

  const handleViewDetails = async (project) => {
    setViewProject(project);
    try {
      const memRes = await api.get(`/api/projects/${project.id}/members`);
      setViewMembers(memRes.data);
      const pubRes = await api.get(`/api/projects/${project.id}/publications`);
      setViewPubs(pubRes.data);
    } catch(e) {}
  };

  const closeViewModal = () => {
    setViewProject(null);
    setViewMembers([]);
    setViewPubs([]);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bạn có chắc chắn muốn xóa Đề tài này? Thao tác không thể hoàn tác!")) return;
    try {
      await api.delete(`/api/projects/${id}`);
      alert("Xóa thành công!");
      fetchProjects();
    } catch (e) {
      alert("Lỗi khi xóa: " + (e.response?.data?.detail || "Lỗi máy chủ"));
    }
  };

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post('/api/projects/', newProject);
      alert('Đăng ký đề tài thành công!');
      setIsModalOpen(false);
      setNewProject({ title: '', research_field: '', start_date: '' });
      fetchProjects();
    } catch (err) {
      alert("Lỗi đăng ký: " + (err.response?.data?.detail || "Lỗi máy chủ"));
    } finally {
      setSubmitting(false);
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
  };

  if (loading) return <div className="loading-spinner">Đang tải dữ liệu JSON...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="table-container">
      <div className="table-header">
        <h3>Danh Sách Đề Tài Nghiên Cứu</h3>
        {user?.role && ['ADMIN', 'TEACHER'].includes(user.role) && (
          <button 
            className="btn-primary" 
            style={{display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', borderRadius: '6px', border: 'none', background: '#3b82f6', color: '#fff', cursor: 'pointer'}}
            onClick={() => setIsModalOpen(true)}
          >
            <FilePlus size={18} /> Đăng ký đề tài
          </button>
        )}
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
                <th>Mã NQL</th>
                <th>Năm</th>
                <th>Trạng thái</th>
                {/* Mở rộng cột thao tác cho mọi người */}
                <th style={{textAlign: 'center'}}>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.id}>
                  <td className="font-medium text-primary">{project.title}</td>
                  <td>{project.research_field}</td>
                  <td className="text-muted text-sm" title={project.leader_id}>
                    {project.leader_id.split('-')[0].toUpperCase()}
                  </td>
                  <td>{new Date(project.start_date).getFullYear()}</td>
                  <td>{getStatusBadge(project.status)}</td>
                  
                  <td style={{textAlign: 'center', display: 'flex', gap: '10px', justifyContent:'center'}}>
                    <button className="btn-icon btn-view" onClick={() => handleViewDetails(project)} title="Xem chi tiết">
                      <Eye size={18}/>
                    </button>
                    {user?.role === 'ADMIN' && (
                      <button className="btn-icon btn-danger" onClick={() => handleDelete(project.id)} title="Xóa đề tài">
                        <Trash2 size={18}/>
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* READ-ONLY DETAILS MODAL */}
      {viewProject && (
        <div className="modal-overlay">
          <div className="modal-content" style={{maxWidth: '650px'}}>
            <div className="modal-header">
              <h3>Hồ sơ Đề tài (View)</h3>
              <button className="btn-close" onClick={closeViewModal}>&times;</button>
            </div>
            
            <div style={{marginBottom: '20px'}}>
              <h4 style={{color: 'var(--primary-color)'}}>{viewProject.title}</h4>
              <p style={{marginTop: '5px', color: 'var(--text-muted)'}}>Lĩnh vực: {viewProject.research_field} | Trạng thái: {viewProject.status}</p>
            </div>

            <div style={{display: 'flex', gap: '20px'}}>
              <div style={{flex: 1}}>
                <h5 style={{borderBottom: '1px solid #e2e8f0', paddingBottom:'5px', marginBottom:'10px'}}>Thành Viên</h5>
                <ul style={{listStyle:'none', padding: 0}}>
                  {viewMembers.length === 0 ? <li className="text-muted text-sm">Chưa cập nhật</li> : viewMembers.map(m => (
                    <li key={m.user_id} className="text-sm" style={{marginBottom:'5px'}}>
                      • {m.user?.username || 'Unknown'} <span className="text-muted">({m.role_in_project})</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div style={{flex: 1}}>
                <h5 style={{borderBottom: '1px solid #e2e8f0', paddingBottom:'5px', marginBottom:'10px'}}>Bài báo KQ</h5>
                <ul style={{listStyle:'none', padding: 0}}>
                  {viewPubs.length === 0 ? <li className="text-muted text-sm">Chưa có bài báo</li> : viewPubs.map(p => (
                    <li key={p.id} className="text-sm" style={{marginBottom:'8px'}}>
                      <strong>{p.title}</strong><br/>
                      <span className="text-muted">{p.journal_name} ({new Date(p.publication_date).getFullYear()})</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="modal-actions" style={{marginTop: '30px'}}>
               <button type="button" className="btn-cancel" onClick={closeViewModal}>Đóng</button>
            </div>
          </div>
        </div>
      )}

      {/* CREATE PROJECT MODAL */}
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Đăng ký Đề Tài Mới</h3>
              <button className="btn-close" onClick={() => setIsModalOpen(false)}>&times;</button>
            </div>
            <form onSubmit={handleCreateSubmit} className="modal-form">
              <div className="form-group">
                <label>Tên Đề tài</label>
                <input required type="text" placeholder="Nhập tên đề tài..." value={newProject.title} onChange={e => setNewProject({...newProject, title: e.target.value})} />
              </div>
              <div className="form-group">
                <label>Lĩnh vực nghiên cứu</label>
                <input required type="text" placeholder="Khoa học, ATTT, AI..." value={newProject.research_field} onChange={e => setNewProject({...newProject, research_field: e.target.value})} />
              </div>
              <div className="form-group">
                <label>Ngày bắt đầu dự kiến</label>
                <input required type="date" value={newProject.start_date} onChange={e => setNewProject({...newProject, start_date: e.target.value})} />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-cancel" onClick={() => setIsModalOpen(false)}>Hủy</button>
                <button type="submit" className="btn-submit" disabled={submitting}>
                  {submitting ? 'Đang gửi...' : 'Đăng ký'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProjectList;
