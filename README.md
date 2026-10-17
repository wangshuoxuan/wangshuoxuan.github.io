# 王烁瑄 / Wangshuoxuan · Personal website

**主页：https://wangshuoxuan.github.io/**

[我的博客](https://wangshuoxuan.github.io/blog.html) · [书籍](https://wangshuoxuan.github.io/books.html) · [视频](https://wangshuoxuan.github.io/videos.html) · [文章](https://wangshuoxuan.github.io/articles.html) · [论文](https://wangshuoxuan.github.io/papers.html) · [问题](https://wangshuoxuan.github.io/questions.html) · [应用](https://wangshuoxuan.github.io/apps.html) · [格言](https://wangshuoxuan.github.io/quotes.html) · [联系我](https://wangshuoxuan.github.io/contact.html)

这是一份以写作、阅读与兴趣探索为中心的个人网站。中文与英文页面共享内容，首页只保留本人指定的研究兴趣，不展示科研项目。

## 日常编辑：优先使用可视化后台

**[打开内容编辑器](https://wangshuoxuan.github.io/admin/)** · [首次连接帮助](https://wangshuoxuan.github.io/admin/help.html)

现在可以使用中文表单、分类下拉框和可视化文章编辑器，不必修改 JSON 或 HTML。首次登录由本人创建仅针对本仓库的编辑令牌。详细说明见 CMS-GUIDE.md。实际保存须在首次授权登录后核验。

## 直接维护源文件（供维护者参考）

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

首页简介现在优先从 content/site.json 读取。编辑器脚本由 vendor_cms.py 在构建时下载并校验。

生成页面已提交到仓库，因此下载后可直接双击 `docs/index.html` 预览。以后在 GitHub 上只修改源内容时，自动部署产物会更新，仓库里已提交的生成 HTML 不一定同步变化；网站以最新成功的 Actions 产物为准。下载源码后运行 build.py 可重新生成最新本地页面。

## 本地预览

```text
python -m pip install -r requirements.txt
python build.py
python vendor_cms.py
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

构建阶段使用 Python 与 Markdown 库；公开内容页面仍是静态 HTML / CSS；只有 /admin/ 管理页面加载本地托管的编辑器脚本。空分类和草稿不会被伪装成已完成的内容。公开仓库里的草稿源文件仍可被查看，私密材料请勿提交。

## 个人介绍、联系与多维清单

`content/site.json` 管理头像、简介、研究兴趣和全部兴趣列表；`content/contact.json` 管理按用途填写的联系方式，空项不公开。`content/subjects.json` 提供视频与问题共用的学科。

视频使用内容形式和多选学科；问题使用问题主题、多选学科和探索状态，并支持参考材料、个人思考、总结。`personal.py` 渲染这些栏目，`docs/browse.js` 负责筛选。无 JavaScript 时仍能阅读完整列表。编辑入口都在可视化后台。旧 CV 地址保留为当前个人介绍页。
