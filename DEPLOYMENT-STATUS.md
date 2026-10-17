# 部署状态：已上线，用户名迁移完成

核验日期：2026-10-17（Asia/Shanghai）

- **个人主页：https://wangshuoxuan.github.io/**
- 英文版：https://wangshuoxuan.github.io/en.html
- 源码仓库：https://github.com/wangshuoxuan/wangshuoxuan.github.io
- 发布配置：Deploy from a branch → main → /docs；HTTPS 已启用。
- 首次站点部署成功记录：https://github.com/wangshuoxuan/wangshuoxuan.github.io/actions/runs/38998217046
- 当前站点源码提交：8587dcbe91c615162a50a1af44c5102cff8b979f
- 迁移部署成功记录：https://github.com/wangshuoxuan/wangshuoxuan.github.io/actions/runs/38998836161

## 已核验

使用不带 Cookie、令牌或其他登录凭据的公开 HTTP 请求：中文首页、英文首页、中英文履历、CSS 和 SVG 图标均返回 200。HTML 文本与交付源码一致（本地与远程换行符不同）；CSS 和 SVG 字节一致。浏览器已打开正式网址并确认显示王烁瑄及全部栏目。部署任务结论为 success。

本地检查：5 个 HTML 页面、48 处站内引用通过；中英文首页在 320、768、1440 px 下无横向溢出。导航、语言切换、折叠提示和 CV 链接已检查。

## 访问范围

网站公开，访客不需要 GitHub 账号。上述检查证明本次测试环境可访问，不代表中国大陆各运营商、校园网络及所有境外网络均稳定可达。GitHub 仓库域名 github.com 与站点域名 github.io 的网络可达性也不能相互替代。实际分享前可在日常 Wi-Fi 和手机流量下分别测试。

## 维护

在本仓库修改 docs/index.html、docs/en.html 等文件并提交到 main，即可触发后续部署。操作方法见 README。此次创建的是独立新仓库，没有覆盖其他项目。根目录说明文件不属于 /docs 网站发布内容。

## 个人资料

公开姓名为王烁瑄 / Wangshuoxuan，公开邮箱为 2400012712@stu.pku.edu.cn，均经本人确认或授权。具体经历、论文、年份、阅读记录和正式 CV 仍为明确标注的待补内容，未虚构成果。

## 用户名迁移

2026-10-17，经本人明确确认，GitHub 用户名已由原账号名称改为 wangshuoxuan，仓库同步改名为 wangshuoxuan.github.io。站内与说明文件链接已同步更新。新网址已部署并核验：5 个 HTML 页面的无需登录请求均返回 200，内容与本地源码一致（规范化换行符后比较）。浏览器已确认新域名与更新后的 GitHub 账号链接。上述首次部署记录为迁移前的历史记录。旧个人主页地址没有自动跳转保证，请分享新网址。

## 知识网站扩展

正在部署：13 个导航入口、九类独立内容页面、中英文索引、46 个预设分类与 Markdown 博客自动发布。新增个人收藏与博客均为空，写作模板保持草稿。构建方式将由 main /docs 改为 GitHub Actions。最终结果待工作流与公开 URL 核验。
