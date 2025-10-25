# COMP9001 期末项目 - 悉尼电影院购票系统

[English Version](./README.md) | 中文版

## 项目概述

这是悉尼大学（USYD）COMP9001课程的期末项目。该项目是一个**悉尼电影院购票系统**，具有Web界面，使用PostgreSQL数据库进行数据管理。

## 课程信息

- **大学**: 悉尼大学（USYD）
- **课程代码**: COMP9001
- **项目类型**: 期末项目
- **项目名称**: 悉尼电影院购票系统

## 项目功能

### 核心功能
- 🎬 **电影管理**: 浏览和搜索正在上映的电影
- 👤 **用户系统**: 用户注册、登录和个人资料管理
- 🏢 **电影院管理**: 悉尼多个电影院位置
- 🎫 **预订系统**: 座位选择和票务预订
- 💳 **支付处理**: 安全支付处理
- 📱 **响应式设计**: 移动友好的Web界面

### 用户角色
- **客户**: 浏览电影、预订票务、管理预订
- **员工**: 管理放映、查看预订、客户服务
- **管理员**: 完整系统管理、用户管理、电影院管理

## 技术栈

### 后端
- **框架**: Flask (Python)
- **数据库**: PostgreSQL
- **认证**: 基于会话的密码哈希
- **API**: RESTful API设计

### 前端
- **HTML5**: 语义标记
- **CSS3**: Bootstrap 5响应式设计
- **JavaScript**: 交互式用户界面
- **Font Awesome**: 图标和视觉元素

### 数据库
- **PostgreSQL**: 关系数据库管理
- **表**: 用户、电影院、电影、放映、预订
- **功能**: 外键、索引、触发器

## 项目结构

```
Comp9001_finalproject/
├── README.md              # 项目文档（英文）
├── README_CN.md           # 项目文档（中文）
├── backend/               # Flask后端应用
│   ├── app.py            # 主Flask应用
│   └── routes/           # API路由和蓝图
├── database/              # 数据库脚本和模式
│   ├── schema.sql        # 数据库模式
│   └── init_db.py        # 数据库初始化脚本
├── web/                   # Web前端
│   ├── static/           # 静态资源（CSS、JS）
│   │   ├── css/         # 样式表
│   │   └── js/          # JavaScript文件
│   └── templates/        # HTML模板
└── requirements.txt       # Python依赖
```

## 安装和设置

### 先决条件
- Python 3.8+
- PostgreSQL 12+
- pip (Python包管理器)

### 数据库设置
1. 安装PostgreSQL并创建名为`booking_system`的数据库
2. 在`database/init_db.py`和`backend/app.py`中更新数据库凭据
3. 运行数据库初始化脚本：
```bash
python database/init_db.py
```

### 应用设置
1. 安装Python依赖：
```bash
pip install -r requirements.txt
```

2. 启动Flask应用：
```bash
python backend/app.py
```

3. 访问Web界面：`http://localhost:5001`

## 默认登录凭据

- **管理员**: `admin` / `admin123`
- **员工**: `staff1` / `staff123`
- **客户**: `john_doe` / `customer123`

## 数据库模式

### 核心表
- **users**: 用户账户和个人资料
- **cinemas**: 电影院位置和信息
- **movies**: 电影详情和元数据
- **screenings**: 电影放映时间和可用性
- **bookings**: 票务预订和支付

### 主要功能
- 用户认证和基于角色的访问
- 悉尼各位置电影院管理
- 带评级和类型的电影目录
- 带座位可用性的放映时间表
- 带支付跟踪的预订系统

## API端点

### 认证
- `POST /api/login` - 用户登录
- `POST /api/register` - 用户注册
- `POST /api/logout` - 用户登出

### 电影
- `GET /api/movies` - 列出所有电影
- `GET /api/movies/{id}` - 获取电影详情
- `GET /api/movies/search` - 搜索电影

### 电影院
- `GET /api/cinemas` - 列出所有电影院
- `GET /api/cinemas/{id}` - 获取电影院详情

### 放映
- `GET /api/screenings` - 列出放映
- `GET /api/screenings/movie/{movie_id}` - 获取电影的放映
- `GET /api/screenings/cinema/{cinema_id}` - 获取电影院的放映

### 预订
- `GET /api/bookings` - 列出用户预订
- `POST /api/bookings` - 创建新预订
- `PUT /api/bookings/{id}` - 更新预订
- `DELETE /api/bookings/{id}` - 取消预订

## 开发说明

### 数据库配置
在以下文件中更新数据库连接设置：
- `backend/app.py` - 主应用数据库配置
- `database/init_db.py` - 数据库初始化配置

### 添加新功能
1. 在`database/schema.sql`中更新数据库模式
2. 在`backend/routes/api.py`中添加API路由
3. 在`web/templates/`中创建前端模板
4. 在`web/static/`中更新静态文件

## 贡献

这是COMP9001的大学项目。仅用于学术目的。

## 许可证

此项目是为教育目的而创建的，作为悉尼大学COMP9001课程作业的一部分。

## 联系

有关此项目的问题，请联系课程讲师或参考课程材料。

---

**注意**: 这是一个为学术目的创建的演示项目。它包含示例数据，不适用于生产使用。