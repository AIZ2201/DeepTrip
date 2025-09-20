# DeepTrip 旅游小助手系统

## 项目简介

DeepTrip 是一套集成 AI 路线规划、智能问答、资源预定与服务反馈的智能旅游平台。系统采用分层架构，包含智能体（agent）、后端（backend）、前端（frontend）三大核心模块，支持游客、商户和管理员多角色协作。

- **agent/**：旅游路径规划智能体，负责 AI 行程生成与推荐。
- **deep_trip/backend/**：后端服务，基于 Flask，提供 API、业务逻辑与数据接口。
- **deep_trip/frontend/**：前端页面，采用原生 HTML/CSS/JS，结合 Jinja2 模板，适配后端渲染。
- **deeptrip.sql**：MySQL 数据库建表与初始化脚本。

---

## 技术栈

| 层级      | 技术栈                                                         |
| --------- | -------------------------------------------------------------- |
| 智能体    | Python，路径规划算法，AI 推荐                                  |
| 后端      | Python 3.10+，Flask，Jinja2，MySQL，Redis                      |
| 前端      | HTML5，CSS3，JavaScript (ES6+)，Jinja2，Chart.js，Font Awesome |
| 构建/管理 | npm scripts，ESLint                                            |

---

## 目录结构

```
DeepTrip/
├── agent/                    # 路线规划智能体
├── deep_trip/
│   ├── backend/              # 后端服务
│   └── frontend/             # 前端页面
│       ├── templates/        # Jinja2 模板
│       ├── static/           # 静态资源
│       └── package.json      # 前端依赖与脚本
├── deeptrip.sql              # 数据库脚本
└── README.md
```

---

## 前端说明

前端采用原生 HTML/CSS/JS，结合 Jinja2 模板，适配 Flask 后端，支持多角色多功能：

- 游客端：登录/注册、智能路线规划、AI 问答、资源预定、服务反馈
- 商户端：商户登录/注册、信息上传、用户评价管理
- 管理员端：管理员登录、数据看板、商户审核、数据报表

主要目录：

- `templates/`：页面模板（如用户登录、路线规划、AI 问答、预定、反馈、商户/管理员相关页面）
- `static/css/`：全局样式
- `static/js/`：交互脚本
- `static/images/`：图片资源

---

## 数据库设计

数据库脚本见 `deeptrip.sql`，涵盖用户、商户、行程、预定、评价、管理员等核心表结构。  
主要表包括：`TRAVELLER`、`PATHLIST`、`AIMESSAGE`、`MERCHANT`、`MERCHANTINFO`、`BOOK`、`COMMENT`、`ADMIN`。

---

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- MySQL 8.0
- Redis 7+
- npm

### 安装与运行

1. **克隆仓库**

   ```bash
   git clone https://github.com/your-username/DeepTrip.git
   cd DeepTrip
   ```

2. **初始化数据库**

   ```bash
   mysql -u root -p < deeptrip.sql
   ```

3. **后端启动**

   > ⚠️ 数据库连接信息通过 `deep_trip/backend/db_config.ini` 配置，请根据实际环境修改该文件内容。  
   > 例如：

   ```ini
   [mysql]
   host=yourhost
   user=youruser
   password=password
   db=yourdatabase
   charset=utf8mb4
   ```

   启动方法：在 DeepTrip 外部文件夹下以模块方式启动

   1. 在 DeepTrip 同级目录新建任意文件夹（如 `DeepTripRun`），进入该文件夹。
   2. 确保 DeepTrip 文件夹与当前目录同级。
   3. 执行：

   ```bash
   python -m DeepTrip.deep_trip.backend.app
   ```

4. **前端开发**
   ```bash
   cd deep_trip/frontend
   npm install
   npm run build
   # 或直接由后端渲染模板
   ```

---

> ⚠️ 当前说明：由于 AI views 文件曾回滚，旅游问答中生成的路线暂时无法保存至数据库，后续版本将修复此问题。

---

## 模块文档

DeepTrip 拆分为多个核心模块，每个模块均独立、可扩展、易集成。

- **用户服务**：用户认证、资料管理与偏好存储
- **AI 助手服务**：行程生成、问答与实时旅行洞察
- **预订服务**：酒店、餐厅、景点等预订功能
- **商家服务**：商家入驻、信息管理、用户反馈
- **管理员服务**：平台管理、数据分析、商家审核

---

## 贡献指南

欢迎贡献代码、文档与建议！请提交 Pull Request 前确保代码规范与必要测试。

---

## 许可证

本项目基于 [Apache License 2.0](LICENSE) 开源发布。

---

## 联系方式

- 邮箱：213222111@seu.edu.cn
- GitHub Issues：[提交 Issue](https://github.com/AIZ2201/DeepTrip/issues)

---

Made with ❤️ by the **DeepTrip Team**
