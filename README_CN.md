# 悉尼电影院预订系统

一个全面的电影院预订系统，用于管理电影、影院、场次和用户预订。

**作者**: 周立  
**日期**: 2025年10月10日-29日  
**课程**: COMP9001 - 悉尼大学

## 功能特性

- 🎬 **电影管理**: 浏览电影海报、详情和类型
- 🏛️ **影院管理**: 查看影院位置、设施和影厅布局
- 🎫 **票务预订**: 实时座位选择和票价计算
- 👤 **用户仪表板**: 追踪预订记录、观影历史和账户状态
- 🔧 **管理面板**: 管理影院、电影、场次和影厅
- 🎨 **现代界面**: 暗色主题，流畅动画，响应式设计

## 快速开始

### 系统要求

- Python 3.10 或更高版本
- PostgreSQL 14 或更高版本
- pip (Python 包管理器)

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/yourusername/Comp9001_finalproject.git
cd Comp9001_finalproject
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置数据库**

编辑 `config.ini` 文件，填写数据库凭据：

```ini
[database]
host = localhost
port = 5432
dbname = cinema_db
user = your_username
password = your_password
```

4. **初始化数据库**

创建数据库并导入架构：

```bash
psql -U your_username -d cinema_db -f database/schema.sql
```

5. **填充测试数据**

运行初始化脚本：

```bash
python init_database.py
```

6. **启动应用**

```bash
python app.py
```

7. **访问应用**

- Web界面: http://localhost:5000
- 默认测试账号:
  - 管理员: `admin` / `admin123`
  - 用户: `john_doe` / `customer123`

## 项目结构

```
Comp9001_finalproject/
├── app.py                      # Flask主应用
├── init_database.py           # 数据库初始化脚本
├── config.ini                 # 数据库配置
├── requirements.txt           # Python依赖
├── backend/                   # 后端业务逻辑
│   ├── models/               # 数据库模型类
│   │   ├── user.py
│   │   ├── cinema.py
│   │   ├── movie.py
│   │   ├── screening.py
│   │   ├── cinema_hall.py
│   │   ├── seat.py
│   │   └── booking.py
│   └── services.py           # 业务逻辑服务
├── routes/                    # Flask路由处理器
│   ├── main.py              # 主路由
│   ├── auth.py              # 认证路由
│   ├── cinemas.py           # 影院路由
│   ├── movies.py            # 电影路由
│   ├── screenings.py        # 场次路由
│   ├── dashboard.py         # 用户仪表板路由
│   └── admin.py             # 管理面板路由
├── database/                # 数据库脚本
│   ├── schema.sql           # 数据库架构
│   └── db.py               # 数据库连接和查询
└── web/                     # 前端
    ├── templates/           # HTML模板
    │   ├── admin/          # 管理面板模板
    │   └── errors/         # 错误页面
    └── static/             # CSS和JavaScript
```

## 技术栈

- **后端**: Python 3.10+, Flask 2.3.3
- **数据库**: PostgreSQL with psycopg 3
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **架构**: MVC模式，带服务层

## 主要功能

### 用户功能

- 浏览活跃电影，查看海报和详情
- 查看影院位置和设施
- 实时座位选择
- 追踪预订历史和取消状态
- 个人仪表板统计

### 管理员功能

- 管理影院激活/停用
- 添加新影院和影厅
- 管理电影库和激活状态
- 场次排期和筛选
- 查看所有预订和系统统计

## 数据库架构

- **users**: 用户账户和认证
- **cinemas**: 影院位置和设施
- **movies**: 电影信息和元数据
- **cinema_halls**: 每个影院的影厅配置
- **seats**: 座位布局和按座位类型定价
- **screenings**: 电影场次和排期
- **bookings**: 用户购票
- **seat_bookings**: 预订-座位关系连接表

## 开发

### 开发模式运行

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### 数据库管理

- **架构**: 参见 `database/schema.sql`
- **测试数据**: 运行 `python init_database.py`
- **连接**: 在 `config.ini` 中配置

## 许可证

本项目为教育用途开发，作为悉尼大学 COMP9001 课程作业。

## 联系方式

**作者**: 周立  
**邮箱**: your.email@example.com  
**机构**: 悉尼大学
