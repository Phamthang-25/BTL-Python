import React, { useState, useEffect } from 'react';
import api from './api';
import { Settings, Users, BookOpen, Save, FileText, Clock, PlayCircle, CheckCircle, XCircle } from 'lucide-react';

function MyProjects({ user }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Modal states
  const [activeProject, setActiveProject] = useState(null);
  const [activeTab, setActiveTab] = useState('INFO');
  
  // Tab 1 States (Info)
  const [projectUpdate, setProjectUpdate] = useState({ title: '', research_field: '', status: '' });
  const [updatingInfo, setUpdatingInfo] = useState(false);

  // Tab 2 & 3 States
  const [members, setMembers] = useState([]);
  const [publications, setPublications] = useState([]);
  const [newMember, setNewMember] = useState({ user_id: '', role_in_project: 'MEMBER' });
  const [newPub, setNewPub] = useState({ title: '', journal_name: '', publication_date: '' });

  useEffect(() => {
    fetchMyProjects();
  }, [user]);

  const fetchMyProjects = async () => {
    if (!user) return;
    try {
      setLoading(true);
      const response = await api.get('/api/projects/');
      // Lọc các đề tài do user hiện tại làm chủ nhiệm (hoặc nếu Admin, có cớ chế xem hết nếu cần. 
      // Ở đây ta ép đúng logic Đề tài của tôi -> leader_id phải bằng user.id)
      const myProjs = response.data.filter(p => p.leader_id === user.id);
      setProjects(myProjs);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openManageModal = (project) => {
    setActiveProject(project);
    setProjectUpdate({
      title: project.title,
      research_field: project.research_field,
      status: project.status
    });
    setActiveTab('INFO');
    loadMembers(project.id);
    loadPublications(project.id);
  };

  const closeManageModal = () => {
    setActiveProject(null);
    fetchMyProjects();
  };

  // --- API DATA HYDRATION (TABS) ---
  const loadMembers = async (id) => {
    try {
      const res = await api.get(`/api/projects/${id}/members`);
      setMembers(res.data);
    } catch(e) {}
  };

  const loadPublications = async (id) => {
    try {
       const res = await api.get(`/api/projects/${id}/publications`);
       setPublications(res.data);
    } catch(e) {}
  };

  // --- FORM HANDLERS ---
  const handleUpdateBasicInfo = async (e) => {
    e.preventDefault();
    setUpdatingInfo(true);
    try {
      await api.put(`/api/projects/${activeProject.id}`, projectUpdate);
      alert("Cập nhật thành công!");
    } catch(e) {
      alert("Lỗi: " + (e.response?.data?.detail || ""));
    } finally {
      setUpdatingInfo(false);
    }
  };

  const handleAddMember = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/api/projects/${activeProject.id}/members`, newMember);
      setNewMember({ user_id: '', role_in_project: 'MEMBER'});
      loadMembers(activeProject.id);
    } catch(e) {
      alert("Lỗi: " + (e.response?.data?.detail || "Nhập sai chuẩn UUID hoặc bị Trùng"));
    }
  };

  const handleAddPub = async (e) => {
    e.preventDefault();
      try {
      await api.post(`/api/projects/${activeProject.id}/publications`, newPub);
      setNewPub({ title: '', journal_name: '', publication_date: ''});
      loadPublications(activeProject.id);
    } catch(e) {
      alert("Lỗi server");
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

  if (!user) return null;

  return (
    <div className="table-container">
      <div className="table-header">
        <h3>Đề Tài Của Tôi (Quản trị)</h3>
      </div>
      
      {loading ? (
        <div className="loading-spinner">Đang tải cấu hình Đề tài...</div>
      ) : projects.length === 0 ? (
        <div className="empty-state">Bạn hiện chưa làm Chủ nhiệm cho đề tài nào.</div>
      ) : (
        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Tên đề tài</th>
                <th>Lĩnh vực</th>
                <th>Trạng thái</th>
                <th style={{textAlign: 'center'}}>Quản lý</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.id}>
                  <td className="font-medium text-primary">{project.title}</td>
                  <td>{project.research_field}</td>
                  <td>{getStatusBadge(project.status)}</td>
                  <td style={{textAlign: 'center'}}>
                    <button 
                      className="btn-primary" 
                      style={{padding: '6px 12px', fontSize: '0.85rem', display: 'inline-flex', gap: '5px'}}
                      onClick={() => openManageModal(project)}
                    >
                      <Settings size={14}/> Quản lý
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* COMPREHENSIVE MANAGEMENT MODAL */}
      {activeProject && (
        <div className="modal-overlay">
          <div className="modal-content" style={{maxWidth: '750px', height: '80vh', display: 'flex', flexDirection: 'column'}}>
            <div className="modal-header" style={{marginBottom: 0}}>
              <h3>Config: {activeProject.title}</h3>
              <button className="btn-close" onClick={closeManageModal}>&times;</button>
            </div>
            
            {/* Tab Navigation */}
            <div className="tab-navigation">
              <button className={activeTab === 'INFO' ? 'active' : ''} onClick={() => setActiveTab('INFO')}><Settings size={16}/> Cơ bản</button>
              <button className={activeTab === 'MEMBERS' ? 'active' : ''} onClick={() => setActiveTab('MEMBERS')}><Users size={16}/> Nhân sự</button>
              <button className={activeTab === 'PUBS' ? 'active' : ''} onClick={() => setActiveTab('PUBS')}><BookOpen size={16}/> Bài Báo</button>
            </div>

            {/* Tab Body */}
            <div className="tab-body" style={{flex: 1, overflowY: 'auto', padding: '20px 0'}}>
              
              {/* TAB 1: BASIC INFO */}
              {activeTab === 'INFO' && (
                <form onSubmit={handleUpdateBasicInfo}>
                  <div className="form-group">
                    <label>Tên Đề tài</label>
                    <input type="text" required value={projectUpdate.title} onChange={e=>setProjectUpdate({...projectUpdate, title: e.target.value})}/>
                  </div>
                  <div className="form-group">
                    <label>Lĩnh vực</label>
                    <input type="text" required value={projectUpdate.research_field} onChange={e=>setProjectUpdate({...projectUpdate, research_field: e.target.value})}/>
                  </div>
                  <div className="form-group">
                    <label>Trạng thái Hồ sơ (Giảng viên tự đẩy trình lên duyệt)</label>
                    <select 
                        style={{width: '100%', padding: '10px 14px', borderRadius: '6px', border: '1px solid #cbd5e1'}}
                        value={projectUpdate.status} 
                        onChange={e=>setProjectUpdate({...projectUpdate, status: e.target.value})}
                    >
                      <option value="DRAFT">DRAFT (Bản Nháp)</option>
                      <option value="SUBMITTED">SUBMITTED (Gửi Phê Duyệt / Báo cáo nghiệm thu)</option>
                      {/* Trạng thái APPROVED/COMPLETED về lý thuyết nên do ADMIN xử lý, nhưng ở đây tạm mở cho test */}
                      <option value="APPROVED">APPROVED (Chấp nhận)</option>
                      <option value="COMPLETED">COMPLETED (Hoàn thành)</option>
                    </select>
                  </div>
                  <button type="submit" disabled={updatingInfo} className="btn-primary" style={{marginTop: '10px'}}><Save size={16} style={{position: 'relative', top: '2px', marginRight: '4px'}}/> Lưu cập nhật</button>
                </form>
              )}

              {/* TAB 2: MEMBERS */}
              {activeTab === 'MEMBERS' && (
                <div style={{display: 'flex', gap: '2rem'}}>
                  <div style={{flex: 1}}>
                    <h4>Thành viên hiện tại</h4>
                    <ul style={{marginTop: '10px', listStyle: 'none'}}>
                      {members.map(m => (
                        <li key={m.user_id} style={{padding: '8px 12px', border: '1px solid #e2e8f0', marginBottom: '8px', borderRadius: '6px'}}>
                          <strong>{m.user?.username || m.user_id.split('-')[0]}</strong> - R: <i>{m.role_in_project}</i>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div style={{flex: 1, backgroundColor: '#f8fafc', padding: '15px', borderRadius: '8px', border: '1px solid #e2e8f0'}}>
                    <h4>Gắn Thành Viên Mới</h4>
                    <form onSubmit={handleAddMember} style={{marginTop: '15px'}}>
                      <div className="form-group">
                        <label>ID Tải khoản (Nhập UUID chuẩn)</label>
                        <input type="text" required value={newMember.user_id} onChange={e=>setNewMember({...newMember, user_id: e.target.value})}/>
                      </div>
                      <div className="form-group">
                        <label>Vai trò dự án</label>
                        <select style={{width: '100%', padding: '10px'}} value={newMember.role_in_project} onChange={e=>setNewMember({...newMember, role_in_project: e.target.value})}>
                          <option value="CHAIRMAN">CHAIRMAN</option>
                          <option value="SECRETARY">SECRETARY</option>
                          <option value="MEMBER">MEMBER</option>
                        </select>
                      </div>
                      <button type="submit" className="btn-primary">Gắn</button>
                    </form>
                  </div>
                </div>
              )}

              {/* TAB 3: PUBLICATIONS */}
              {activeTab === 'PUBS' && (
                <div style={{display: 'flex', gap: '2rem'}}>
                  <div style={{flex: 1}}>
                    <h4>Danh sách Bài Báo / Báo cáo</h4>
                    <div style={{marginTop: '10px'}}>
                      {publications.map(p => (
                         <div key={p.id} style={{padding: '10px', border: '1px solid #e2e8f0', marginBottom: '8px', borderRadius: '6px'}}>
                           <div style={{fontWeight: 600, color: 'var(--primary-color)'}}>{p.title}</div>
                           <div style={{fontSize: '0.85rem'}}>Tạp chí: {p.journal_name} - Năm: {new Date(p.publication_date).getFullYear()}</div>
                         </div>
                      ))}
                    </div>
                  </div>
                  <div style={{flex: 1, backgroundColor: '#f8fafc', padding: '15px', borderRadius: '8px', border: '1px solid #e2e8f0'}}>
                    <h4>Gắn Thùng Báo Cáo</h4>
                    <form onSubmit={handleAddPub} style={{marginTop: '15px'}}>
                      <div className="form-group"><label>Tên bài báo</label><input type="text" required value={newPub.title} onChange={e=>setNewPub({...newPub, title: e.target.value})}/></div>
                      <div className="form-group"><label>Tạp chí / Nơi công bố</label><input type="text" required value={newPub.journal_name} onChange={e=>setNewPub({...newPub, journal_name: e.target.value})}/></div>
                      <div className="form-group"><label>Ngày công bố</label><input type="date" required value={newPub.publication_date} onChange={e=>setNewPub({...newPub, publication_date: e.target.value})}/></div>
                      <button type="submit" className="btn-primary">Khai báo</button>
                    </form>
                  </div>
                </div>
              )}

            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MyProjects;
