# 电影推荐系统

一个基于 Flask + Python 的电影信息抓取和推荐网站，整合 TMDB 和豆瓣电影数据，提供个性化观影推荐。

## 功能特点

- **今日推荐**: 每天自动推荐高分电影，基于日期生成固定推荐
- **热门电影排行**: 实时获取当前热门电影和评分
- **即将上映**: 查看即将上映的新片预告
- **类型偏好推荐**: 根据喜好的电影类型（动作、喜剧、科幻等）获取个性化推荐
- **电影详情**: 点击电影卡片查看详细信息，包括简介、评分、上映日期等

## 技术栈

- **后端**: Python 3.x + Flask
- **前端**: HTML5 + CSS3 + JavaScript (原生)
- **数据源**: TMDB API、豆瓣电影
- **依赖库**: requests, beautifulsoup4, flask-cors

## 安装步骤

### 1. 克隆项目

```bash
cd movie_recommendation
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 TMDB API Key

1. 访问 [TMDB 官网](https://www.themoviedb.org/) 注册账号
2. 在 [API 设置页面](https://www.themoviedb.org/settings/api) 申请 API Key
3. 设置环境变量或直接修改 `app.py` 中的 API Key:

**方式一：环境变量（推荐）**
```bash
# Windows
set TMDB_API_KEY=your_api_key_here

# Linux/Mac
export TMDB_API_KEY=your_api_key_here
```

**方式二：直接修改代码**
在 `app.py` 中找到这一行：
```python
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', 'YOUR_TMDB_API_KEY')
```
将 `YOUR_TMDB_API_KEY` 替换为你的实际 API Key。

### 4. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 项目结构

```
movie_recommendation/
├── app.py                  # Flask 应用主文件
├── requirements.txt        # Python 依赖列表
├── README.md              # 项目说明文档
├── templates/
│   └── index.html         # 前端 HTML 页面
└── static/
    ├── css/
    │   └── style.css      # 样式文件
    └── js/
        └── app.js         # 前端 JavaScript 逻辑
```

## API 接口说明

### 1. 获取热门电影
```
GET /api/movies/hot
```

### 2. 获取即将上映
```
GET /api/movies/upcoming
```

### 3. 获取今日推荐
```
GET /api/movies/daily
```

### 4. 获取类型推荐
```
POST /api/movies/recommend
Content-Type: application/json

{
  "genres": ["动作", "科幻", "冒险"]
}
```

## 使用说明

1. **浏览今日推荐**: 打开网站即可看到今日推荐的电影
2. **查看热门排行**: 点击"热门电影"标签查看当前热门电影
3. **查看即将上映**: 点击"即将上映"标签了解新片信息
4. **个性化推荐**:
   - 点击"类型推荐"标签
   - 选择喜欢的电影类型（可多选）
   - 点击"获取推荐"按钮
5. **查看详情**: 点击任何电影卡片查看详细信息

## 注意事项

1. **TMDB API 限制**: 免费账户有请求频率限制，建议适度使用
2. **豆瓣数据**: 豆瓣 API 需要授权，当前版本主要使用 TMDB 数据
3. **网络连接**: 需要稳定的网络连接以获取电影数据
4. **跨域问题**: 已配置 flask-cors 解决跨域问题

## 功能扩展建议

- 添加用户登录和收藏功能
- 实现观影计划日历
- 增加电影评论和讨论功能
- 添加数据缓存以提高加载速度
- 集成更多数据源（IMDb、烂番茄等）
- 添加 AI 推荐算法

## 常见问题

### Q: 无法加载电影数据？
A: 检查以下几点：
- TMDB API Key 是否正确配置
- 网络连接是否正常
- 是否超过 API 请求限制

### Q: 图片无法显示？
A: TMDB 图片服务器可能需要科学上网，或图片链接失效。

### Q: 如何获取豆瓣数据？
A: 豆瓣 API 需要申请，或可以使用爬虫技术（需遵守网站 robots.txt 规则）。

## 开源协议

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。
