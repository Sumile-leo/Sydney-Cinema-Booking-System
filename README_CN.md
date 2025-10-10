# COMP9001 期末项目 - 购票系统

[English Version](./README.md) | 中文版

## 项目简介

这是悉尼大学（University of Sydney）COMP9001课程的期末项目。本项目是一个**购票系统**，包含桌面GUI界面和Web网页界面，使用MySQL数据库进行数据管理。

## 课程信息

- **学校**: 悉尼大学 (University of Sydney)
- **课程代码**: COMP9001
- **项目类型**: Final Project (期末项目)
- **项目名称**: 购票系统 (Ticket Booking System)

## 项目特色

### 核心功能
- 🎫 **票务管理**: 浏览和搜索活动/演出信息
- 👤 **用户系统**: 用户注册、登录和个人信息管理
- 🛒 **订票系统**: 选择座位和购买票务
- 📋 **订单管理**: 查看订单历史和票据详情
- 🔐 **管理后台**: 活动管理和订单统计

### 技术亮点
- 🖥️ **桌面应用**: 使用PyQt5构建（现代化美观GUI）
- 🌐 **Web应用**: 基于Flask的轻量级Web应用
- 💾 **数据库**: MySQL数据持久化
- 🎨 **现代化UI**: 专业且用户友好的界面设计

## 项目结构

```
Comp9001_finalproject/
├── README.md              # 项目说明文档（英文）
├── README_CN.md           # 项目说明文档（中文）
├── backend/               # Flask后端应用
│   └── routes/           # API路由和蓝图
├── database/              # 数据库脚本和架构
├── desktop/               # 桌面GUI应用（PyQt5）
└── web/                   # Web前端
    ├── static/           # 静态资源（CSS、JS）
    │   ├── css/         # 样式文件
    │   └── js/          # JavaScript文件
    └── templates/        # HTML模板
```

## 技术栈

- **编程语言**: Python 3.x
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
python desktop/main.py
```

#### Web应用
```bash
python backend/app.py
```
然后在浏览器中访问：`http://localhost:5000`

## 开发指南

### 分支管理

- `main`: 主分支，存放稳定的生产代码
- `dev`: 开发分支，用于日常开发
- `feature/*`: 功能分支，用于开发新功能
- `bugfix/*`: 错误修复分支

### 提交规范

遵循约定式提交格式：

```
<type>: <subject>

<body>
```

**类型（type）：**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或辅助工具的变动

### 编码规范

- 遵循PEP 8 Python代码风格指南
- 使用有意义的变量和函数名
- 为复杂逻辑添加注释
- 为函数和类编写文档字符串

## 项目进度

- [x] 项目初始化和仓库搭建
- [x] 项目结构设计
- [ ] 数据库架构设计
- [ ] 后端API开发
- [ ] 桌面GUI实现
- [ ] Web前端开发
- [ ] 测试和调试
- [ ] 文档完善
- [ ] 最终部署

## 团队成员

- [您的姓名](GitHub链接)

## 数据库设计

系统使用以下主要数据表：

- **users**: 用户账户和身份验证
- **events**: 活动/演出信息
- **orders**: 票务订单和交易
- **seats**: 座位可用性和价格

详细架构请参考 `database/schema.sql`

## API文档

（随开发进度添加）

## 测试

```bash
# 运行单元测试
python -m pytest tests/

# 运行测试并生成覆盖率报告
python -m pytest --cov=backend tests/
```

## 故障排除

### 常见问题

1. **数据库连接错误**: 检查MySQL服务状态和凭据配置
2. **模块未找到**: 确保通过 `pip install -r requirements.txt` 安装了所有依赖
3. **端口已被占用**: 在配置中更改端口号

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'feat: 添加某个功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目仅用于学术目的，是悉尼大学COMP9001课程要求的一部分。

## 联系方式

- **GitHub Issues**: [项目Issues页面](https://github.com/Sumile-leo/Comp9001_finalproject/issues)
- **邮箱**: your.email@university.edu.au

## 致谢

特别感谢：
- COMP9001课程的讲师和助教们
- 悉尼大学提供的学习资源
- 开源社区提供的各种工具和库

## 项目截图

（完成后添加）

---

**学术诚信声明**: 本项目作为COMP9001的原创作品提交。所有代码均由项目团队编写。请保持学术诚信，不要抄袭。

**最后更新**: 2025年10月10日
