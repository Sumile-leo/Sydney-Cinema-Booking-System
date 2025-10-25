# COMP9001 期末项目提案
# 购票系统 (Ticket Booking System)

## 项目概述

### 项目名称
**购票系统 (Ticket Booking System)**

### 课程信息
- **学校**: 悉尼大学 (University of Sydney)
- **课程代码**: COMP9001
- **项目类型**: Final Project (期末项目)
- **提交截止**: 2025年11月2日
- **学生**: 周力

### 项目描述
一个综合性的票务预订和管理系统，提供桌面GUI界面和Web网页界面，用于购买活动票务。系统允许用户浏览活动、选择座位、购买票务，并通过直观的界面管理订单。

## 项目动机

### 为什么选择这个项目？
1. **实际应用价值**: 票务预订系统广泛应用于娱乐、体育和活动行业
2. **技术多样性**: 结合桌面GUI开发、Web开发和数据库管理
3. **用户体验导向**: 强调现代化UI/UX设计原则
4. **可扩展性**: 可扩展用于不同类型的活动和场馆

### 学习目标
- 掌握PyQt5的Python GUI开发
- 学习Flask框架的Web开发
- 理解数据库设计和管理
- 实现用户认证和会话管理
- 实践软件工程原则

## 技术架构

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   桌面GUI界面   │    │   Web前端界面   │    │   移动应用      │
│   (PyQt5)       │    │   (HTML/CSS/JS) │    │   (未来扩展)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Flask API     │
                    │   (后端服务)    │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   MySQL 数据库  │
                    │   (数据存储)    │
                    └─────────────────┘
```

### 技术栈
- **前端**: PyQt5 (桌面), HTML5/CSS3/JavaScript (Web)
- **后端**: Flask (Python Web框架)
- **数据库**: MySQL
- **认证**: 基于会话的认证
- **API**: RESTful API设计

## 核心功能

### 1. 用户管理
- **用户注册**: 创建新用户账户
- **用户登录/登出**: 安全的认证系统
- **个人资料管理**: 更新用户信息
- **密码重置**: 基于邮件的密码恢复

### 2. 活动管理
- **活动列表**: 浏览可用活动/演出
- **活动详情**: 查看活动信息、场馆、时间
- **活动搜索**: 按类别、日期、地点筛选活动
- **活动分类**: 音乐会、体育、戏剧、电影等

### 3. 订票系统
- **座位选择**: 交互式座位图显示可用性
- **票务类型**: 不同价格等级（VIP、标准、经济）
- **购物车**: 结账前添加多张票
- **支付处理**: 安全的支付集成
- **订票确认**: 邮件/短信确认

### 4. 订单管理
- **订单历史**: 查看过去和当前的预订
- **票务详情**: 下载/查看数字票
- **订单修改**: 取消或修改预订（在政策范围内）
- **退款处理**: 处理取消请求

### 5. 管理后台
- **活动管理**: 创建、更新、删除活动
- **用户管理**: 查看用户账户和活动
- **订单统计**: 销售报告和分析
- **场馆管理**: 管理座位安排

## 数据库设计

### 核心数据表

#### 用户表
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 活动表
```sql
CREATE TABLE events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    venue VARCHAR(100) NOT NULL,
    event_date DATETIME NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 订单表
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    seat_numbers VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);
```

#### 座位表
```sql
CREATE TABLE seats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    seat_type ENUM('VIP', 'Standard', 'Economy') DEFAULT 'Standard',
    price DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE KEY unique_seat (event_id, seat_number)
);
```

## 实施计划

### 第一阶段：后端开发（第1周）
**时间**: 2025年10月10-16日

#### 数据库设置
- [ ] 设计和创建数据库架构
- [ ] 设置MySQL数据库
- [ ] 创建数据库连接模块
- [ ] 实现数据库初始化脚本

#### Flask API开发
- [ ] 设置Flask应用结构
- [ ] 实现用户认证端点
- [ ] 创建活动管理API
- [ ] 开发订票系统API
- [ ] 添加订单管理端点

#### 核心后端功能
- [ ] 用户注册和登录
- [ ] 密码哈希和安全
- [ ] 会话管理
- [ ] 输入验证和错误处理
- [ ] API文档

### 第二阶段：桌面应用（第2周）
**时间**: 2025年10月17-23日

#### PyQt5 GUI开发
- [ ] 设计主应用窗口
- [ ] 创建登录/注册对话框
- [ ] 实现活动浏览界面
- [ ] 开发座位选择界面
- [ ] 构建订票确认对话框

#### 桌面功能
- [ ] 用户认证集成
- [ ] 活动列表和搜索
- [ ] 交互式座位图
- [ ] 购物车功能
- [ ] 订单历史查看器
- [ ] 管理员面板界面

#### UI/UX设计
- [ ] 现代化直观界面
- [ ] 响应式设计元素
- [ ] 自定义样式和主题
- [ ] 错误处理和用户反馈
- [ ] 无障碍功能

### 第三阶段：Web前端和集成（第3周）
**时间**: 2025年10月24日 - 11月2日

#### Web界面开发
- [ ] 创建响应式HTML模板
- [ ] 实现CSS样式
- [ ] 添加JavaScript功能
- [ ] 开发用户认证页面
- [ ] 构建活动浏览界面

#### 前后端集成
- [ ] 连接Web前端到Flask API
- [ ] 实现AJAX动态内容
- [ ] 添加实时座位可用性
- [ ] 集成支付处理
- [ ] 处理会话管理

#### 测试和优化
- [ ] 后端单元测试
- [ ] 集成测试
- [ ] 用户验收测试
- [ ] 性能优化
- [ ] 错误修复和改进

## 挑战和解决方案

### 技术挑战

#### 1. 数据库并发
**挑战**: 处理同时座位预订
**解决方案**: 实现数据库事务和锁定机制

#### 2. 实时更新
**挑战**: 保持座位可用性实时性
**解决方案**: 使用WebSocket或轮询进行实时更新

#### 3. 支付集成
**挑战**: 安全支付处理
**解决方案**: 集成成熟的支付网关（Stripe、PayPal）

#### 4. 可扩展性
**挑战**: 处理热门活动的高流量
**解决方案**: 实现缓存和数据库优化

### 设计挑战

#### 1. 用户体验
**挑战**: 为桌面和Web创建直观界面
**解决方案**: 遵循现代UI/UX原则并进行用户测试

#### 2. 跨平台兼容性
**挑战**: 确保跨平台一致体验
**解决方案**: 使用响应式设计和跨平台测试

## 成功标准

### 功能要求
- [ ] 用户可以成功注册和登录
- [ ] 可以浏览和搜索活动
- [ ] 可以选择和预订座位
- [ ] 可以处理和确认订单
- [ ] 管理员可以管理活动和用户
- [ ] 系统正确处理并发预订

### 技术要求
- [ ] 应用程序运行无崩溃
- [ ] 数据库操作高效
- [ ] API响应快速（< 2秒）
- [ ] 代码文档完善且可维护
- [ ] 遵循安全最佳实践

### 用户体验要求
- [ ] 界面直观易用
- [ ] 加载时间可接受
- [ ] 错误信息清晰有用
- [ ] 应用在不同屏幕尺寸下工作

## 测试策略

### 单元测试
- 测试单个函数和方法
- 验证数据库操作
- 测试API端点
- 验证输入处理

### 集成测试
- 测试桌面-后端集成
- 测试Web-后端集成
- 验证数据库连接
- 测试支付处理

### 用户验收测试
- 测试完整用户工作流
- 验证所有功能按预期工作
- 测试错误场景
- 验证用户体验

### 性能测试
- 测试多并发用户
- 验证数据库性能
- 测试API响应时间
- 验证内存使用

## 资源和工具

### 开发工具
- **IDE**: Visual Studio Code / PyCharm
- **版本控制**: Git / GitHub
- **数据库**: MySQL Workbench
- **GUI设计**: Qt Designer
- **API测试**: Postman

### 学习资源
- PyQt5文档
- Flask文档
- MySQL文档
- Python最佳实践
- UI/UX设计原则

### 外部服务
- **支付网关**: Stripe / PayPal（未来集成）
- **邮件服务**: SMTP / SendGrid（通知）
- **云托管**: AWS / Heroku（部署）

## 风险评估

### 技术风险
- **数据库性能**: 大数据集查询缓慢的风险
  - *缓解措施*: 实现适当的索引和查询优化
- **安全漏洞**: 数据泄露或未授权访问的风险
  - *缓解措施*: 遵循安全最佳实践和定期安全审计
- **集成问题**: 连接不同组件时出现问题的风险
  - *缓解措施*: 彻底测试和逐步集成

### 时间风险
- **功能蔓延**: 添加过多功能的风险
  - *缓解措施*: 坚持核心要求和MVP方法
- **技术困难**: 遇到复杂问题的风险
  - *缓解措施*: 从简单实现开始并迭代
- **测试时间**: 测试时间不足的风险
  - *缓解措施*: 在整个开发过程中持续测试

### 资源风险
- **学习曲线**: 花费过多时间学习新技术的风险
  - *缓解措施*: 尽可能使用熟悉的技术
- **外部依赖**: 第三方服务失败的风险
  - *缓解措施*: 制定备份计划和备用选项

## 结论

购票系统项目代表了一个综合应用程序，展示了软件开发多个领域的熟练程度。通过结合桌面GUI开发、Web开发和数据库管理，这个项目展示了Python和现代Web技术的多功能性。

项目的实际应用价值使其成为展示实用软件工程技能的绝佳选择。模块化架构允许未来的扩展和改进，使其成为宝贵的学习经验和作品集。

通过仔细规划、系统开发和彻底测试，这个项目将成功满足所有要求，并为理解全栈应用开发提供坚实的基础。

---

**项目时间线**: 2025年10月10日 - 11月2日（3周）
**总预估时间**: 60-80小时
**复杂度级别**: 中级到高级