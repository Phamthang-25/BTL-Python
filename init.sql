CREATE TYPE user_role AS ENUM ('ADMIN', 'TEACHER', 'STUDENT');
CREATE TYPE project_status AS ENUM ('DRAFT', 'SUBMITTED', 'APPROVED', 'COMPLETED', 'REJECTED');
CREATE TYPE project_member_role AS ENUM ('CHAIRMAN', 'MEMBER', 'SECRETARY');


-- Bảng Users (Giảng viên/Sinh viên)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'STUDENT',
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(100), -- VD: 'Mật mã', 'An ninh mạng', 'An toàn hệ thống thông tin'...
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Projects (Đề tài Nghiên cứu Khoa học)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    research_field VARCHAR(100) NOT NULL, -- VD: 'Blockchain Security', 'Pentest', 'Cryptography'
    budget DECIMAL(15, 2) DEFAULT 0.00,
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    status project_status DEFAULT 'DRAFT',
    leader_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Khóa ngoại: Người chủ nhiệm phải là một user đã tồn tại
    -- ON DELETE RESTRICT: Tránh vô tình xóa User đang là chủ nhiệm đề tài
    CONSTRAINT fk_leader FOREIGN KEY (leader_id) REFERENCES users(id) ON DELETE RESTRICT,
    
    -- Constraint (Ràng buộc logic): Ngày kết thúc phải sau hoặc bằng ngày bắt đầu
    CONSTRAINT check_dates CHECK (end_date >= start_date)
);

-- Bảng ProjectMembers (Bảng trung gian N-N giữa Users và Projects)
CREATE TABLE project_members (
    user_id UUID NOT NULL,
    project_id UUID NOT NULL,
    role_in_project project_member_role NOT NULL DEFAULT 'MEMBER',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Khóa chính kép (Composite Primary Key) đảm bảo 1 user không bị lặp tên trong 1 project
    PRIMARY KEY (user_id, project_id),
    
    -- Khóa ngoại
    -- ON CASCADE: Nếu user hoặc project bị xóa, bản ghi trung gian cũng bị xóa theo
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Bảng Publications (Bài báo khoa học/Hội thảo)
CREATE TABLE publications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    journal_name VARCHAR(255) NOT NULL,
    publication_date DATE NOT NULL,
    file_url TEXT, -- Link minh chứng bài báo (S3 URL, Drive, etc.)
    project_id UUID, -- Optional: Có thể nối hoặc không nối với dự án
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Khóa ngoại
    -- ON DELETE SET NULL: Nếu đề tài bị xóa, bài báo vẫn còn lưu nhưng không còn gắn với đề tài đó nữa
    CONSTRAINT fk_project_pub FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);


-- Tối ưu hóa việc tìm user bằng email (khi login)
CREATE INDEX idx_users_email ON users(email);

-- Tối ưu hóa việc filter (lọc) dự án theo trạng thái, hoặc theo chủ nhiệm đề tài
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_leader_id ON projects(leader_id);

-- Tối ưu hóa việc lấy danh sách công bố của một đề tài
CREATE INDEX idx_publications_project_id ON publications(project_id);
