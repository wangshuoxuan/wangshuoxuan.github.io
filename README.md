# Personal homepage · 王烁瑄 / Wangshuoxuan

一个文字优先、中英文双语的个人主页 MVP。背景为北京大学微电子与经济学，研究兴趣为忆阻器、存算一体与神经形态计算。

**已上线：[个人主页](https://wangshuoxuan.github.io/) · [English](https://wangshuoxuan.github.io/en.html)**

仓库：[wangshuoxuan/wangshuoxuan.github.io](https://github.com/wangshuoxuan/wangshuoxuan.github.io)。已配置 `main /docs` 发布，后续编辑并提交即可更新。核验记录见 `DEPLOYMENT-STATUS.md`。

**当前内容是可编辑底稿。** 公开姓名已确认为王烁瑄 / Wangshuoxuan；wangshuoxuan 是已核实的 GitHub 用户名。学位、年份、项目经历、文章、阅读记录和正式 CV 尚待补充。公开邮箱已按本人授权设置为 2400012712@stu.pku.edu.cn。未编造论文、奖项、实验结果或熟练掌握的技能。

## 立即预览

双击 `docs/index.html` 即可打开中文首页。点击 English 查看英文版。无须安装任何框架、依赖或构建工具。

也可以在本目录运行 `python -m http.server 8080 --directory docs`，然后打开 `http://localhost:8080`。这是本地预览，不是公网发布。

## 文件结构

```text
personal-homepage/
├── README.md              维护与发布说明
├── CONTENT-CHECKLIST.md   待补资料与内容写作模板
├── DESIGN.md              参考风格与设计决策
├── DEPLOYMENT-STATUS.md   本次部署状态及核验结果
├── .gitignore
└── docs/                  GitHub Pages 发布目录
    ├── index.html         中文首页：主要编辑入口
    ├── en.html            英文首页：与中文同步维护
    ├── cv.html            中文履历框架（不是正式 CV）
    ├── cv-en.html         英文履历框架（不是正式 CV）
    ├── 404.html           找不到页面时的提示
    ├── styles.css         布局、字体、配色、打印样式
    ├── favicon.svg        原创文字图标
    └── .nojekyll          关闭不必要的 Jekyll 处理
```

## 从零部署或迁移时参考（本站已完成，无须重做）

1. 登录 `wangshuoxuan`，打开 <https://github.com/new>。
2. 新建公开仓库 **`wangshuoxuan.github.io`**。不要选择或覆盖已有项目。若该名称已存在，先检查其中内容；有已有内容时改用独立仓库名，例如 `personal-homepage`。
3. 上传本目录中的内容，保留 `docs` 这一层；仓库中应出现 `docs/index.html`，而不是 `personal-homepage/docs/index.html`。**不要上传 ZIP 本身。** 可先创建带 README 的仓库，再用 Add file → Upload files 上传 `docs` 文件夹及其他说明文件。已有 README 不必覆盖，可在后续合并说明。
4. 打开仓库 **Settings → Pages**。在 Build and deployment 中选择 **Deploy from a branch**，分支选 **main**，目录选 **/docs**，保存。
5. 等待 Pages 部署任务结束，按 Settings → Pages 显示的 **Visit site** 打开网站。标准用户站点预期地址为 <https://wangshuoxuan.github.io/>。本站已完成部署并核验该地址；重新部署时仍以 Pages 状态与实际页面为准。
6. 如果采用 `personal-homepage` 仓库，预期地址为 `https://wangshuoxuan.github.io/personal-homepage/`。主页、语言切换和 CV 使用相对路径，可在两种地址下运行；但应把 `docs/404.html` 的返回主页链接改成实际站点地址。

如果网页上传忽略了隐藏文件，在 GitHub 创建 `docs/.nojekyll` 空文件即可。即使遗漏，它也不影响当前普通 HTML/CSS 的核心展示；保留它可以明确表示纯静态发布。

GitHub 官方说明：
- [创建 Pages 网站](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [配置发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 日常维护：只需改 HTML

在 GitHub 打开相应文件，点击铅笔图标 Edit，修改后 Commit changes；若 Pages 已设为 `main /docs`，后续提交会触发重新发布。手机上也可以用 GitHub 网页编辑。

| 要修改的内容 | 修改位置 |
|---|---|
| 姓名 / 简介 | `docs/index.html` 与 `docs/en.html`，搜索 `EDIT`、`王烁瑄` / `Wangshuoxuan` 或 `id="about"` |
| 研究方向 | 两个首页中的 `id="research"` |
| 项目 | 两个首页中的 `id="projects"` |
| 文章 / 笔记 | 两个首页中的 `id="writing"` |
| 阅读记录 | 两个首页中的 `id="reading"` |
| 邮箱 | 两个首页与 CV 页中的 Contact / 联系方式 |
| 简历 | `docs/cv.html` 和 `docs/cv-en.html`；或上传正式 PDF 并替换链接 |
| 配色、间距、字号 | `docs/styles.css` 顶部变量和对应样式 |
| 最后更新时间 | 两个首页页脚中的 `2026.10.17` / `17 Oct 2026` |

**姓名与账号是两回事。** 替换公开姓名时，只改显示姓名、网页标题和页脚署名，不要把 `https://github.com/wangshuoxuan` 中的账号也替换成姓名。英文拼写已由本人确认为 Wangshuoxuan。经济学的主修/双学位/辅修身份尚未确认，当前只写学习领域。

HTML 的 `<标签>` 与 `</标签>` 配对保留，只修改其中的文字。正文里的 `&` 写成 `&amp;`，`<` 写成 `&lt;`。图片使用相对路径、写好 `alt` 文字，不依赖本机绝对路径。中英文为两个独立静态文件，修改事实时请同步两边。

### 添加项目

复制 `Projects` 中现有的 `<article class="project">…</article>`，填写真实项目名称与状态。优先说明问题、个人贡献、方法和可核验结果。新增记录后删除相应的 `.placeholder` 块；若暂不公开项目，保留当前明确标注的占位即可。

### 添加文章

在 `docs/` 新建 HTML 页面，例如 `note-001.html`，可以复制 CV 页的基本结构，替换标题、正文和语言信息；删除 CV 的 `noindex` 标签及不适用的语言替代链接。在 Writing 栏添加标题、摘要和 `<a href="note-001.html">阅读全文</a>`。单独上传 Markdown 不会自动变成设计一致的文章页面。

### 添加阅读记录

填写作品、作者、来源链接、阅读状态及自己的判断。不把推荐书目或计划阅读写成已经读过，不把 AI 的摘要直接写成个人读后感。

### 添加正式 CV

当前履历框架可直接编辑、打印，页面明确标注“不完整”。完成并核实后，用浏览器打印为 PDF，保存为 `docs/cv.pdf`。将首页 `href="cv.html"` / `href="cv-en.html"` 改为 `href="cv.pdf"`，同时把链接文字改成“下载 CV（PDF）” / “Download CV (PDF)”。**不要只改按钮文字而未上传文件。** 中文和英文 CV 也可以各上传一份并分别链接。

### 修改公开邮箱

当前已按本人授权公开 2400012712@stu.pku.edu.cn。修改时，在两个首页及两个 CV 页中同时更新 `mailto:` 链接地址和显示文字；不要只改显示文字。

## 发布后核验

- 用无痕窗口打开公开 URL，确认访客无需登录。
- 分别查看手机与电脑，点击七个目录链接、English / 中文及 CV 链接。
- 在仓库 Actions 中确认 `pages build and deployment` 已完成。
- 修改后若未立即更新，等待部署完成再刷新。GitHub 文档提示更新可能需要约 10 分钟。
- 若 404，检查仓库公开性、`main /docs` 配置，以及 `docs/index.html` 是否确实在所选分支。
- 自定义域名以后再配置；现在无需购买域名。公网 URL 可访问不等于所有地区或网络都始终畅通。

## 技术与内容边界

纯 HTML/CSS，无 JavaScript、追踪器、外部字体、数据库、表单或账号系统。导航与折叠提示使用浏览器原生功能，关闭脚本也可阅读。所有核心资源随站点一起托管。

本版由 AI 辅助设计、起草与实现，个人文案可继续改写。参考站点只用于学习内容组织原则，没有复制其源代码、文章、照片或个人经历。未引入第三方素材许可证负担，也未替你选择整个个人资料的开源许可。
