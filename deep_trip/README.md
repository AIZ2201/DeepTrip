# 旅游小助手系统 - 前端代码

## 项目简介

旅游小助手系统是一个集旅游路线规划、旅游问答、资源预定和服务反馈于一体的综合平台。系统分为游客端、商户端和管理员端三大模块，为用户提供全方位的旅游服务支持。

## 技术栈

- **前端框架**：HTML5 + CSS3 + JavaScript
- **模板引擎**：Jinja2 (用于与后端 Flask/FastAPI 集成)
- **样式**：原生 CSS + Font Awesome 图标
- **图表库**：Chart.js
- **构建工具**：npm scripts
- **代码规范**：遵循 ES6 标准

## 项目结构

```
frontend/
├── templates/            # Jinja2 模板文件
│   ├── layout.html       # 基础布局模板
│   ├── user_login.html   # 用户登录页面
│   ├── user_register.html # 用户注册页面
│   ├── route_planner.html # 旅游路线规划页面
│   ├── ai_chat.html      # 旅游问答页面
│   ├── booking.html      # 资源预定页面
│   ├── feedback.html     # 服务反馈页面
│   ├── merchant_login.html # 商户登录页面
│   ├── merchant_register.html # 商户注册页面
│   ├── merchant_info_upload.html # 商户信息上传页面
│   ├── merchant_feedback.html # 商户反馈查看页面
│   ├── admin_login.html  # 管理员登录页面
│   ├── admin_dashboard.html # 旅游数据查询页面
│   ├── admin_merchant_review.html # 商户审核页面
│   └── admin_data_report.html # 数据报表页面
├── static/               # 静态资源文件
│   ├── css/              # CSS 样式文件
│   │   └── styles.css    # 全局样式表
│   ├── js/               # JavaScript 文件
│   │   └── scripts.js    # 基础交互脚本
│   └── images/           # 图片资源目录
└── package.json          # 项目配置和依赖管理
```

## 功能模块

### 一、游客端功能

1. **登录/注册页面**：用户邮箱、密码输入框，支持注册新账号。
2. **旅游路线规划页面**：输入出行条件（时间、预算、人数、兴趣标签），显示 AI 生成的多条推荐路线。
3. **旅游问答页面**：类似聊天界面，用户可输入问题，AI 返回旅游相关答案。
4. **资源预定页面**：酒店、景区、餐饮列表展示，提交预定请求并返回订单信息。
5. **服务反馈页面**：用户对已体验的服务进行评分与评论（支持图文上传）。

### 二、商户端功能

1. **商户登录/注册页面**：商户邮箱、密码注册与登录。
2. **店铺信息上传页面**：表单上传店铺名称、地址、营业时间、服务项目等信息。
3. **商户反馈查看页面**：显示用户对店铺的评价和评分，商户可进行公开回复。

### 三、管理员端功能

1. **管理员登录页面**：管理员账号与密码输入。
2. **旅游数据查询页面**：可视化看板展示热门景点、酒店、餐饮、商户数据。
3. **商户审核页面**：展示商户提交的信息，管理员审核（通过/不通过）。
4. **数据报表页面**：按时间维度生成用户、商户、订单数据报表，支持导出 Excel/PDF。

## 安装与运行

### 前提条件

- Node.js (建议 v14.0 或更高版本)
- npm (Node.js 包管理器)

### 安装步骤

1. **克隆项目代码**

   ```bash
   git clone [项目仓库地址]
   cd deep_trip
   ```

2. **安装依赖**

   ```bash
   cd frontend
   npm install
   ```

3. **构建项目**

   ```bash
   npm run build
   ```

   构建完成后，前端静态资源将生成在指定的构建目录中（可在 package.json 中配置）。

4. **与后端集成**

   前端代码使用 Jinja2 模板引擎，需要与 Flask 或 FastAPI 后端框架集成。后端服务应配置正确的模板目录和静态文件目录。

## 开发指南

### 代码规范

- HTML 结构遵循语义化原则
- CSS 样式采用模块化设计，避免全局污染
- JavaScript 代码使用 ES6+ 特性，保持代码简洁高效
- 命名规范：文件和变量使用小写字母，单词之间用连字符(-)分隔
- 注释：关键代码段添加必要的注释说明

### 开发模式

在开发过程中，可以使用以下命令启动开发服务器（需要后端支持）：

```bash
npm run dev
```

### 代码检查

项目使用 ESLint 进行代码质量检查：

```bash
npm run lint
```

## 浏览器兼容性

系统支持以下主流浏览器：

- Chrome (推荐最新稳定版)
- Firefox (推荐最新稳定版)
- Safari (推荐最新稳定版)
- Edge (推荐最新稳定版)
- IE 11 (部分功能可能受限)

## 注意事项

1. 前端代码需要与后端 API 配合使用，确保后端服务已正确配置并运行。
2. 部分功能（如语音识别）预留了接口，需要后端提供相应服务。
3. 图表功能依赖 Chart.js 库，确保正确引入。
4. 页面使用响应式设计，可适应不同屏幕尺寸。

# 启动后端与前后端连接说明

## 一、后端启动方法

1. 进入 backend 目录：

   ```bash
   cd backend
   ```

2. 安装依赖（建议使用虚拟环境）：

   ```bash
   pip install -r requirements.txt
   ```

3. 启动 FastAPI 服务（默认端口 8000）：
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   - `--reload` 便于开发调试，生产环境可去掉。
   - 启动后访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 可查看 API 文档。

## 二、前后端连接方式

- **模板渲染模式（如 Flask/Jinja2）**  
  前端页面通过后端渲染，直接访问如 `/user/login`、`/merchant/login` 等路由即可。

- **API 模式（推荐，前后端分离）**  
  前端页面通过 AJAX/Fetch/axios 等方式请求后端 API（如 `/api/v1/users/login`），后端返回 JSON 数据，前端根据数据动态渲染页面。

### 连接示例

- 前端登录表单提交到 `/api/v1/users/login`，后端处理并返回结果。
- 前端通过 `fetch` 或 `axios` 访问后端 API，例如：
  ```js
  fetch("http://127.0.0.1:8000/api/v1/users/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      /* 处理登录结果 */
    });
  ```

### 注意事项

- 前端开发时如有跨域问题，确保后端已配置 CORS（`main.py` 已配置允许所有来源）。
- 生产环境建议将 `allow_origins` 设置为你的前端实际域名。
- 前端静态资源和模板可由 Flask/FastAPI 提供，也可用独立 Web 服务器（如 Nginx）托管。

---

**总结：**

- 后端用 `uvicorn` 启动 FastAPI 服务。
- 前端通过 HTTP 请求（API 或模板渲染）与后端通信。
- 推荐前后端分离开发，接口通过 `/api/v1/...` 访问。

如需具体某一端的启动命令或代码示例，可继续提问。

# FastAPI 后端启动与测试方法

## 启动后端服务

1. 打开命令行，进入 backend 目录（如有虚拟环境请先激活）：

   ```bash
   cd backend
   ```

2. 安装依赖（只需首次或依赖变更时）：

   ```bash
   pip install -r requirements.txt
   ```

3. 启动 FastAPI 服务（开发模式）：

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   - `--reload` 支持热重载，便于开发调试。

4. 打开浏览器访问接口文档：
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) （Swagger UI）
   - [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) （ReDoc）

## 测试 API

- 直接在 `/docs` 页面可以在线测试所有已注册的 API。
- 也可以用 Postman、curl、httpie 等工具测试接口。

## 常见问题

- **端口被占用**：换一个端口，如 `--port 8080`
- **依赖未安装**：请确保已执行 `pip install -r requirements.txt`
- **模块找不到**：请确保当前目录为 backend，且目录结构正确。

---

如需测试前端与后端联调，请确保前端请求的 API 地址与后端一致（如 `http://127.0.0.1:8000/api/v1/users/login`）。

## License

[MIT](LICENSE)

# 如何使用终端运行后端服务

1. 打开命令行（终端），进入 backend 目录（确保路径为 deep_trip\backend）：

   ```bash
   cd deep_trip\backend
   ```

2. 安装依赖（只需首次或依赖变更时）：

   ```bash
   pip install -r requirements.txt
   ```

3. 启动 FastAPI 服务（推荐从 deep_trip 目录启动，确保包导入无误）：

   ```bash
   cd ..
   uvicorn backend.main:app --reload
   ```

   或者（如果你就在 backend 目录下，也可以这样）：

   ```bash
   uvicorn main:app --reload
   ```

4. 打开浏览器访问接口文档：
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

**注意事项：**

- 推荐在 `deep_trip` 目录下运行 `uvicorn backend.main:app --reload`，这样包导入最稳定。
- 如果遇到导入错误，检查 `__init__.py` 文件和启动路径。
