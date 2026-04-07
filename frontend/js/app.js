// ===== CONFIG =====
const API_URL = "http://localhost:8000/api";

// ===== XỬ LÝ LOGIN =====
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const user = document.getElementById('username').value;
        const pass = document.getElementById('password').value;
        const errMsg = document.getElementById('errorMsg');
        
        try {
            const res = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: user, password: pass })
            });
            const data = await res.json();
            
            if (data.success) {
                // Lưu thẳng thông tin vào localStorage để các trang sau biết ai đang đăng nhập
                localStorage.setItem('user_id', data.user.id);
                localStorage.setItem('user_role', data.user.role);
                localStorage.setItem('username', data.user.username);
                window.location.href = 'dashboard.html';
            } else {
                errMsg.innerText = data.message;
                errMsg.style.display = 'block';
            }
        } catch (err) {
            errMsg.innerText = "Lỗi kết nối tới máy chủ!";
            errMsg.style.display = 'block';
            console.error(err);
        }
    });
}

// ===== KIỂM TRA ĐĂNG NHẬP (TRÊN DASHBOARD) =====
function checkAuthAndLoadData() {
    const userId = localStorage.getItem('user_id');
    const role = localStorage.getItem('user_role');
    const name = localStorage.getItem('username');
    
    if (!userId) {
        window.location.href = 'login.html'; // Đuổi về trang login nếu chưa đăng nhập
        return;
    }

    // Hiển thị tên và quyền
    document.getElementById('userNameLabel').innerText = name;
    document.getElementById('userRoleBadge').innerText = role;

    // Hiển thị các chức năng tùy theo quyền
    if (role === 'ADMIN') document.getElementById('adminPanel').style.display = 'block';
    if (role === 'TEACHER') document.getElementById('teacherPanel').style.display = 'block';

    // Tải danh sách đề tài
    loadProjects();
}

function logout() {
    localStorage.clear();
    window.location.href = 'login.html';
}

// Hàm fetch tự động gắn header X-User-Id và X-User-Role do không có JWT
async function fetchAPI(endpoint, options = {}) {
    if (!options.headers) options.headers = {};
    options.headers['X-User-Id'] = localStorage.getItem('user_id');
    options.headers['X-User-Role'] = localStorage.getItem('user_role');
    options.headers['Content-Type'] = 'application/json';
    
    const res = await fetch(`${API_URL}${endpoint}`, options);
    return res.json();
}

// ===== API GỌI DATA ĐỀ TÀI =====
async function loadProjects() {
    const projects = await fetchAPI('/projects');
    const tbody = document.getElementById('projectsBody');
    const role = localStorage.getItem('user_role');
    tbody.innerHTML = '';
    
    projects.forEach(p => {
        let actionButtons = '';
        
        // ADMIN: Có nút Duyệt / Hủy
        if (role === 'ADMIN') {
            if (p.status !== 'APPROVED') actionButtons += `<button class="btn btn-success btn-sm" onclick="changeStatus('${p.id}', 'APPROVED')">Duyệt</button> `;
            if (p.status !== 'REJECTED') actionButtons += `<button class="btn btn-sm" style="background:red; color:white;" onclick="changeStatus('${p.id}', 'REJECTED')">Hủy</button>`;
        }
        
        // TEACHER: Có nút xem danh sách sinh viên xin tham gia
        if (role === 'TEACHER') {
            actionButtons += `<button class="btn btn-primary btn-sm" onclick="viewRequests('${p.id}')">Xem Sinh viên y/cầu</button>`;
        }
        
        // STUDENT: Nút xin tham gia
        if (role === 'STUDENT') {
            actionButtons += `<button class="btn btn-success btn-sm" onclick="applyProject('${p.id}')">Xin tham gia</button>`;
        }

        tbody.innerHTML += `
            <tr>
                <td><b>${p.title}</b><br><span style="font-size:12px;color:gray">${p.status}</span></td>
                <td>${p.leader_name}</td>
                <td>${p.start_date || 'Chưa định'}</td>
                <td><span class="badge" style="background:#eee">${p.status}</span></td>
                <td>${actionButtons}</td>
            </tr>
        `;
    });
}

// Admin: Duyệt đề tài
async function changeStatus(projectId, newStatus) {
    if(!confirm("Đổi trạng thái thành: " + newStatus + "?")) return;
    await fetchAPI(`/projects/${projectId}/status`, { method: 'PUT', body: JSON.stringify({status: newStatus}) });
    loadProjects();
}

// Giảng viên tạo đề tài
async function createProject() {
    const title = document.getElementById('newTitle').value;
    const date = document.getElementById('newDate').value;
    if(!title || !date) return alert("Nhập đủ tên và ngày!");
    
    await fetchAPI('/projects', { method: 'POST', body: JSON.stringify({title: title, start_date: date}) });
    document.getElementById('addProjectForm').style.display='none';
    loadProjects();
}

// Sinh viên xin tham gia
async function applyProject(projectId) {
    const out = await fetchAPI('/requests', { method: 'POST', body: JSON.stringify({project_id: projectId}) });
    if(out.success) alert("Đã gửi yêu cầu thành công!");
    else alert(out.message || "Lỗi");
}

// Giảng viên xem danh sách sinh viên xin dự án
async function viewRequests(projectId) {
    const reqs = await fetchAPI(`/requests/project/${projectId}`);
    document.getElementById('requestsPanel').style.display = 'block';
    
    const panel = document.getElementById('requestsBody');
    panel.innerHTML = '<ul style="padding-left:15px; margin-bottom:10px;">' + reqs.map(r => `
        <li style="margin-bottom:5px;">
            <b>${r.username}</b> (${r.status}) 
            ${r.status === 'PENDING' ? `
                <button class="btn btn-success btn-sm" onclick="changeRequestStatus('${r.project_id}','${r.user_id}','APPROVED')">Duyệt</button>
                <button class="btn btn-sm" style="background:red;color:white" onclick="changeRequestStatus('${r.project_id}','${r.user_id}','REJECTED')">Từ chối</button>
            ` : ''}
        </li>
    `).join('') + '</ul>';
    
    if(reqs.length === 0) panel.innerHTML = "Chưa có sinh viên nào yêu cầu.";
}

async function changeRequestStatus(pId, uId, status) {
    await fetchAPI(`/requests/${pId}/${uId}/status`, { method: 'PUT', body: JSON.stringify({status: status}) });
    viewRequests(pId);
}

// --- ADMIN TÍNH NĂNG THÊM ---
async function fetchUsers() {
    const users = await fetchAPI('/users');
    let html = `
        <table class="table" style="font-size:13px;">
            <tr style="background:#ddd"><th>Username</th><th>Role</th><th>Email</th><th></th></tr>
    `;
    users.forEach(u => {
        html += `<tr>
            <td>${u.username}</td><td>${u.role}</td><td>${u.email}</td>
            <td><button class="btn btn-sm" style="background:red;color:white" onclick="deleteUser('${u.id}')">Xóa</button></td>
        </tr>`;
    });
    html += `</table>`;
    document.getElementById('usersListContent').innerHTML = html;
}

async function deleteUser(id) {
    if(confirm("Chắc chắn xóa?")) {
        await fetchAPI(`/users/${id}`, {method: 'DELETE'});
        fetchUsers();
    }
}
