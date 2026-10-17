# 如何给这个网站持续添内容

现在优先使用 [可视化编辑器](https://wangshuoxuan.github.io/admin/)，无需手改以下源文件。首次连接见 CMS-GUIDE.md。下文保留给维护者作格式参考。

网站地址：https://wangshuoxuan.github.io/

侧边栏有 13 个入口，分为关于我、写作与思考、收藏与推荐，另有独立的联系页面。你提出的九项都有独立入口。书籍、视频、文章、论文、问题、应用和格言共预设 46 个可修改的分类；它们是整理框架，不代表你已经读过、使用过或推荐过其中任何作品。

## 写博客：新增一个 Markdown 文件即可

在 GitHub 仓库打开 `content/posts/first-post.md`，这是尚未发布的模板。可以编辑它，或在 `content/posts/` 新建另一个 `.md` 文件。文件顶部保留下面七行信息：

```markdown
---
title: 文章标题
date: 2026-10-17
summary: 用一两句话说明文章在讨论什么。
category: essay
lang: zh
draft: true
---

## 从一个问题开始

这里写正文。可以使用列表、引用、表格、脚注和代码块。
```

写好后将 `draft: true` 改为 `draft: false`，提交到 `main`。网站会自动生成文章页面、博客索引和 Atom 订阅源，不必手工写 HTML 或修改目录。

- 文件名采用英文小写和连字符，如 `why-data-movement-matters.md`；公开 URL 为 `post-why-data-movement-matters.html`，以后尽量不改文件名。
- `category` 可用 `research`（研究笔记）、`essay`（随笔）、`reading`（阅读札记），其他值归入其他写作。
- `lang` 使用 `zh` 或 `en`。中文、英文博客索引均收录文章原文，不自动翻译你的写作。
- `date` 使用 `YYYY-MM-DD`。它用于排序，不提供定时发布；未来日期配合 `draft: false` 也会立即发布。
- 元数据是简单的 `key: value` 格式；`draft` 只能写小写 `true` 或 `false`，不要加引号。复杂标题可用双引号包住，并按 JSON 字符串规则处理内部引号。
- 顶部 `title` 已生成一级标题，正文从 `##` 二级标题开始，避免多出一个 H1。
- 图片可上传到 `docs/assets/`，正文用 `![图片说明](assets/文件名.jpg)`。
- `draft: true` 只会阻止内容进入公开网站和订阅源。**本仓库公开，草稿源文件在 GitHub 上仍可见。私人写作请先保存在本地。**
- 已公开文章改回草稿后，下一次部署会移除生成的文章页和订阅条目；这不撤销别人已经保存的副本或 Git 历史。

RSS / Atom 地址：https://wangshuoxuan.github.io/feed.xml

## 添收藏：编辑对应的 JSON 文件

| 内容 | 文件 | 网站入口 |
|---|---|---|
| 书籍 | `content/books.json` | `books.html` |
| 视频 | `content/videos.json` | `videos.html` |
| 文章收藏 | `content/articles.json` | `articles.html` |
| 论文 | `content/papers.json` | `papers.html` |
| 感兴趣的问题 | `content/questions.json` | `questions.html` |
| 应用与工具 | `content/apps.json` | `apps.html` |
| 格言 | `content/quotes.json` | `quotes.html` |

每个文件有 `categories`（分类）和 `entries`（条目）。在 `entries` 的空数组里添加对象；多项之间使用英文逗号。JSON 用英文双引号，不支持注释，也不要保留最后一项后多余的逗号。

下面仅是格式示例，不会自动显示为你的推荐：

```json
{
  "category": "computing",
  "title": {"zh": "在这里填写真实标题", "en": "Optional English title"},
  "creator": "作者或创作者",
  "year": "年份",
  "url": "https://example.com/replace-with-the-source",
  "status": {"zh": "待读", "en": "To read"},
  "note": {"zh": "说明它解决什么问题，以及为什么值得看。"},
  "tags": ["一个主题", "另一个主题"],
  "draft": true
}
```

`category` 必须与本文件已有分类的 `id` 一致。准备公开后，把 `draft` 改成 `false`；不写 `draft` 时条目默认公开。题目必填，来源链接如提供必须以 `https://` 或 `http://` 开头。标题、说明、作者等纯文本会被自动转义，避免把文本意外当成页面代码。

推荐理由不要只写“很好”，优先写“适合谁、解决什么问题、需要什么背景、有什么局限”。材料的质量和你对它的判断，可以分别记录。

### 不同类型值得多记的字段

- **书籍**：作者、版本、阅读状态、一个核心观点和一个保留意见。拥有、待读、在读、读完与推荐是不同状态。
- **视频**：用 `format` 写播客 / 演讲 / 课程 / 中短视频，`duration` 写实际时长；系列课程可给课程主页，片段可在链接中带合法时间戳。
- **文章**：作者 / 公众号、日期与原始链接。微信文章保留原链接即可，站点不抓取全文；部分来源可能要求在微信内打开或登录原平台。
- **论文**：作者、年份、论文类型与 DOI / 出版社 / arXiv 等原始入口。预印本与同行评议论文应分别注明，可在 `status` 中记录“待读 / 精读 / 待复现”。
- **问题**：`title` 直接写问题，`note` 写为什么重要、什么证据可能改变判断；`status` 可写开放 / 研究中 / 已更新，来源链接可省略。
- **应用**：用途、适合谁、实际使用情况及限制；不要把计划尝试写成已经长期使用。价格和隐私条件会变化，涉及它们时可在说明里写核验日期。
- **格言**：除标题和分类外，必须有 `quote`（原话）及 `url`（可核查出处），建议 `creator` 写作者，`note` 写语境。不能确定出处的句子先留草稿。不要大段转载仍受版权保护的原文。

### 修改分类

在 `categories` 中添加或改写分类的 `name` 与 `description`。`id` 采用英文小写和连字符，保持稳定；如果修改已有 `id`，同时更新引用它的条目。同一份内容会生成中英文索引；没有提供英文说明时不假装已经翻译。

## 改主页与联系信息

主页正文源文件是 `content/home-zh.html`、`content/home-en.html`。导航与收藏页由 `build.py` 统一生成，**不要只编辑生成后的 `docs/index.html` 或收藏页**，否则下次构建会被源文件覆盖。

联系页面的姓名、邮箱和 GitHub 信息在 `build.py` 中维护；履历仍在 `docs/cv.html`、`docs/cv-en.html` 中直接编辑。样式在 `docs/styles.css`。侧边栏目录只需改 `build.py` 的 `navigation()`，所有生成页面会同步。

## 自动发布失败时

打开仓库 Actions → Publish personal website → 最新运行，查看失败的 Build 或 Check 步骤。通常是 JSON 逗号、分类 id、日期格式或 Markdown 顶部字段写错。构建失败时不会替换已成功上线的版本。

本地检查：安装 `requirements.txt` 中的依赖，运行 `python build.py` 和 `python check_site.py`，再用 `python -m http.server 8080 --directory docs` 预览。
