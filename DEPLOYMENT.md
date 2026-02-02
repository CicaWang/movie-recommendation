# 部署到 Render 指南

## 快速部署步骤

### 1. 准备 GitHub 仓库

首先需要将项目上传到 GitHub：

```bash
cd movie_recommendation

# 初始化 git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Movie Recommendation System"

# 在 GitHub 上创建新仓库，然后关联
git remote add origin https://github.com/你的用户名/movie-recommendation.git
git branch -M main
git push -u origin main
```

### 2. 在 Render 上部署

1. **注册 Render 账号**
   - 访问 https://render.com/
   - 点击右上角 "Get Started" 注册（可以用 GitHub 账号直接登录）

2. **创建新的 Web Service**
   - 登录后，点击 "New +" 按钮
   - 选择 "Web Service"
   - 连接你的 GitHub 账号
   - 选择刚才创建的仓库 `movie-recommendation`

3. **配置部署设置**
   - **Name**: `movie-recommendation`（或其他你喜欢的名字）
   - **Region**: 选择离你最近的区域
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: 选择 `Free`

4. **添加环境变量**
   - 在 "Environment" 部分，点击 "Add Environment Variable"
   - 添加以下变量：
     - Key: `TMDB_API_KEY`
     - Value: `你的TMDB API密钥`

   如果还没有 TMDB API Key：
   - 访问 https://www.themoviedb.org/
   - 注册账号
   - 进入 Settings > API > 申请 API Key
   - 选择 "Developer" 类型
   - 填写简单的申请信息即可获得

5. **部署**
   - 点击 "Create Web Service"
   - Render 会自动开始构建和部署
   - 等待 5-10 分钟完成部署

6. **获取网址**
   - 部署成功后，你会看到类似这样的网址：
   - `https://movie-recommendation-xxxx.onrender.com`
   - 这就是你的电影推荐网站！

## 注意事项

- **免费套餐限制**: Render 免费套餐会在 15 分钟无活动后休眠，首次访问可能需要等待 30-60 秒唤醒
- **持久化**: 免费套餐不支持持久化存储，每次重启会重置
- **流量限制**: 每月 400 小时免费运行时间

## 更新网站

当你需要更新代码时：

```bash
# 修改代码后
git add .
git commit -m "更新说明"
git push

# Render 会自动检测到更新并重新部署
```

## 替代方案

如果 Render 部署遇到问题，还可以尝试：

### Railway
- 网址: https://railway.app/
- 同样支持 GitHub 一键部署
- 免费套餐: 每月 $5 额度

### PythonAnywhere
- 网址: https://www.pythonanywhere.com/
- 专门针对 Python 应用
- 免费套餐限制较多但稳定

## 故障排除

### 部署失败
- 检查 requirements.txt 是否正确
- 查看 Render 的 Logs 了解错误信息

### 网站无法访问
- 确认 TMDB_API_KEY 环境变量已正确设置
- 检查 Render 服务状态是否为 "Live"

### 数据加载慢
- 免费套餐休眠后首次访问较慢
- 可以考虑添加 loading 提示

## 获取帮助

如有问题，可以：
- 查看 Render 文档: https://render.com/docs
- 检查应用日志: Render Dashboard > Logs
- GitHub Issues: 提交问题到项目仓库
