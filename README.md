# 王烁瑄 / Wangshuoxuan · Personal website

**主页：https://wangshuoxuan.github.io/**

[我的博客](https://wangshuoxuan.github.io/blog.html) · [书籍](https://wangshuoxuan.github.io/books.html) · [视频](https://wangshuoxuan.github.io/videos.html) · [文章](https://wangshuoxuan.github.io/articles.html) · [论文](https://wangshuoxuan.github.io/papers.html) · [问题](https://wangshuoxuan.github.io/questions.html) · [应用](https://wangshuoxuan.github.io/apps.html) · [格言](https://wangshuoxuan.github.io/quotes.html) · [联系我](https://wangshuoxuan.github.io/contact.html)

这是一份以文字、持续写作和可核验内容为中心的个人网站。中文与英文页面共享导航与内容分类。当前新增收藏页只有分类框架，没有把未经本人确认的条目写成个人推荐，也没有自动发布任何个人博客。

## 最常用的两种维护方式

**写博客：**在 `content/posts/` 新增 Markdown 文件，填写标题、日期和摘要，写好后设 `draft: false`，提交到 main。GitHub Actions 会生成文章、更新博客索引和 RSS / Atom，并重新发布。

**添推荐：**编辑 `content/books.json`、`videos.json`、`articles.json`、`papers.json`、`questions.json`、`apps.json` 或 `quotes.json` 的 entries 数组，提交后自动发布。分类、作者、来源、推荐理由、阅读状态、视频时长与标签均可记录。

**完整格式与示例见 [CONTENT-GUIDE.md](CONTENT-GUIDE.md)。**

## 文件在哪里

| 文件 | 作用 |
|---|---|
| `content/home-zh.html`、`content/home-en.html` | 主页正文源文件 |
| `content/*.json` | 各类收藏及分类，是后续编辑入口 |
| `content/posts/*.md` | 个人博客与笔记，含未发布模板 |
| `build.py` | 统一生成导航、收藏页、博客与订阅源 |
| `docs/styles.css` | 暖白、深绿、窄栏文字排版及手机适配 |
| `docs/cv.html`、`docs/cv-en.html` | 尚未补全的履历框架，可直接编辑 |
| `docs/*.html` | 可直接打开的生成页面；其中生成页不应单独编辑 |
| `docs/feed.xml` | 自动生成的 Atom 订阅源 |
| `requirements.txt` | 构建时使用的固定版本 Markdown 库 |
| `.github/workflows/publish.yml` | 构建、验证并部署网站 |
| `check_site.py`、`test_build.py` | 链接检查与发布行为验证 |
| `CONTENT-CHECKLIST.md` | 学术简介、项目和履历的待补资料 |
| `DESIGN.md` | 参考来源与设计决策 |

生成页面已提交到仓库，因此下载后可直接双击 `docs/index.html` 预览。以后在 GitHub 上只修改源内容时，自动部署产物会更新，仓库里已提交的生成 HTML 不一定同步变化；网站以最新成功的 Actions 产物为准。下载源码后运行 build.py 可重新生成最新本地页面。

## 本地预览

```text
python -m pip install -r requirements.txt
python build.py
python check_site.py
python -m unittest test_build.py
python -m http.server 8080 --directory docs
```

打开 http://localhost:8080 。本地地址不是公网网址。

## 发布与故障排查

本站使用 **Settings → Pages → Source: GitHub Actions**，由 Publish personal website 工作流从 main 构建并发布 docs。已经配置的仓库不需要重新创建。

如果复制或迁移本项目：启用 Actions；设置 Pages Source 为 GitHub Actions；确保 github-pages 环境允许 main 分支部署；提交内容或在 Actions 中手动运行工作流。

提交后在 Actions 查看构建是否成功。JSON 格式、无效日期、错误分类、缺失引用会让构建失败，失败的产物不会发布。公开站点无需访客登录，但不保证所有地区和运营商都稳定可达。

官方参考：[GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 内容边界

公开姓名：王烁瑄 / Wangshuoxuan；GitHub：wangshuoxuan；公开邮箱：2400012712@stu.pku.edu.cn，均经本人确认或授权。学位、年份、论文、奖项和具体研究结果未猜填。

构建阶段使用 Python 与 Markdown 库；浏览器运行时仍是静态 HTML / CSS，没有外部字体、追踪器或 JavaScript 依赖。空分类和草稿不会被伪装成已完成的内容。公开仓库里的草稿源文件仍可被查看，私密材料请勿提交。
