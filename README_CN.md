# COMP9001 期末项目 - 购票系统

[English Version](./README.md) | 中文版

## 项目简介

这是悉尼大学（University of Sydney）COMP9001课程的期末项目。本项目是一个**购票系统**，包含桌面GUI界面和Web网页界面，使用MySQL数据库进行数据管理。

## 课程信息

- **学校**: 悉尼大学 (University of Sydney)
- **课程代码**: COMP9001
- **项目类型**: Final Project (期末项目)
- **项目名称**: Ticket Booking System (购票系统)
- **提交截止**: 2025年11月2日

## 项目特色

### 🎫 核心功能
- **活动管理**: 浏览和搜索活动/演出信息
- **用户系统**: 用户注册、登录和个人信息管理
- **订票系统**: 选择座位和购买票务
- **订单管理**: 查看订单历史和票据详情
- **管理后台**: 活动管理和订单统计

### 技术亮点
- 🖥️ **桌面应用**: 使用PyQt5构建（现代化美观GUI）
- 🌐 **Web应用**: 基于Flask的轻量级Web应用
- 💾 **数据库**: MySQL数据持久化
- 🎨 **现代化UI**: 专业且用户友好的界面设计

## 项目结构

```
Comp9001_finalproject/
├── README.md                  # 项目说明文档（英文）
├── README_CN.md               # 项目说明文档（中文）
├── PROJECT_SUMMARY.md          # 项目简要描述
├── requirements.txt            # Python依赖包
├── .gitignore                  # Git忽略文件
├── main.py                     # 应用入口
├── backend/                    # Flask后端应用
│   ├── __init__.py
│   ├── app.py                  # Flask应用
│   ├── models.py               # 数据库模型
│   ├── routes/                 # API路由
│   └── config.py              # 配置文件
├── desktop/                    # 桌面GUI应用（PyQt5）
│   ├── __init__.py
│   ├── main_window.py          # 主GUI窗口
│   ├── login_dialog.py         # 登录对话框
│   ├── booking_window.py       # 订票界面
│   └── admin_panel.py          # 管理员界面
├── database/                   # 数据库脚本和架构
│   ├── schema.sql              # 数据库架构
│   └── init_db.py              # 数据库初始化
├── web/                        # Web前端
│   ├── static/                 # 静态资源（CSS、JS）
│   │   ├── css/                # 样式文件
│   │   └── js/                 # JavaScript文件
│   └── templates/              # HTML模板
├── assets/                     # 游戏资源（可选）
│   ├── sounds/                 # 音效文件
│   └── music/                  # 背景音乐
├── docs/                       # 附加文档
│   └── particle_demo.py         # 粒子演示（参考）
└── tests/                      # 测试代码
```

## 技术栈

- **编程语言**: Python 3.8+
- **Web框架**: Flask
- **桌面GUI**: PyQt5
- **数据库**: MySQL
- **前端**: HTML5, CSS3, JavaScript
- **其他库**: 
  - PyMySQL / mysql-connector-python（数据库驱动）
  - Flask-SQLAlchemy（ORM，可选）
  - PyQt5 Designer（GUI设计工具）
  - 其他需要的Python库

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- MySQL Server 5.7 或更高版本
- pip（Python包管理器）
- Git

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/Sumile-leo/Comp9001_finalproject.git
   cd Comp9001_finalproject
   ```

2. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置MySQL数据库**
   - 启动MySQL服务
   - 创建数据库并导入架构
   - 在配置文件中更新数据库配置

4. **初始化数据库**
   ```bash
   python database/init_db.py
   ```

### 运行应用

#### 桌面应用
```bash
python desktop/main_window.py
```

#### Web应用
```bash
python backend/app.py
```
然后在浏览器中访问：`http://localhost:5000`

## 开发进度

- [x] 项目初始化和仓库搭建
- [x] 项目文档和提案
- [ ] 第1周：数据库设计和后端API
- [ ] 第2周：桌面GUI实现
- [ ] 第3周：Web前端和集成

## 开发时间线

### 第1周（10月10-16日）：后端开发
- 数据库架构设计
- Flask API开发
- 用户认证系统
- 活动和订单管理

### 第2周（10月17-23日）：桌面应用
- PyQt5 GUI设计
- 用户界面实现
- 订票系统集成
- 管理员面板开发

### 第3周（10月24日 - 11月2日）：Web前端和优化
- Web界面开发
- 前后端集成
- 测试和调试
- 文档和演示

## 数据库设计

系统使用以下主要数据表：

- **users**: 用户账户和身份验证
- **events**: 活动/演出信息
- **orders**: 票务订单和交易
- **seats**: 座位可用性和价格

详细架构请参考 `database/schema.sql`

## 学习成果

本项目展示了：

**Python编程:**
- 面向对象设计（用户、活动、订单类）
- 数据结构（管理对象集合）
- 数据库操作（CRUD操作）
- Web开发（Flask框架）

**GUI开发:**
- PyQt5高级功能
- 自定义UI组件
- 事件处理（用户交互）
- 桌面应用架构

**数据库管理:**
- 关系数据库设计
- SQL查询和操作
- 数据关系和约束
- 数据库优化

**软件工程:**
- 模块化设计
- 代码组织
- API开发
- 文档编写

## 团队成员

- 周力 - [GitHub](https://github.com/Sumile-leo)

## 致谢

特别感谢：
- COMP9001课程的讲师和助教们
- 悉尼大学提供的学习资源
- Flask和PyQt5社区提供的文档和支持

## 许可证

本项目仅用于学术目的，是悉尼大学COMP9001课程要求的一部分。

## 联系方式

- **GitHub仓库**: [Comp9001_finalproject](https://github.com/Sumile-leo/Comp9001_finalproject)
- **GitHub Issues**: [报告问题](https://github.com/Sumile-leo/Comp9001_finalproject/issues)
- **邮箱**: your.email@university.edu.au

---

**学术诚信声明**: 本项目作为COMP9001的原创作品提交。所有代码均由项目作者编写。请保持学术诚信。

**最后更新**: 2025年10月10日