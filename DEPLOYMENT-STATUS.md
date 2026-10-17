# 部署状态：知识网站已上线

核验日期：2026-10-17（Asia/Shanghai）

- 主页：https://wangshuoxuan.github.io/
- 源码仓库：https://github.com/wangshuoxuan/wangshuoxuan.github.io
- 构建与部署：GitHub Actions → Publish personal website
- 已核验的站点源码：51656fcf7793d2242f944a546c479da692ee2857
- 成功工作流：https://github.com/wangshuoxuan/wangshuoxuan.github.io/actions/runs/39001512057
- 访问方式：公开 HTTPS，访客不需要登录。

## 本版内容

13 个导航入口；书籍、视频、文章收藏、论文、问题、博客、应用、格言、联系我九项都有独立页面；中英文索引；46 个可修改分类。收藏与个人博客尚无已确认的公开条目，写作模板保持草稿。没有将示例内容或 AI 推荐伪装成作者经历、阅读记录或个人观点。

## 核验

- 5 项发布行为测试通过，包括文章发布与撤回、草稿排除、条目文字转义、来源链接校验与格言出处要求。
- 23 个 HTML 页面、818 处站内引用、Atom 文件通过检查。
- 六类页面在真实 320 与 1440 像素宽度下均无横向溢出；手机目录已展开并操作跳转。
- GitHub Actions 的构建和部署均成功。
- 25 个公开页面或资源使用不带登录凭据的请求访问，均返回 200，规范化换行后与本地文件一致。

这是本次测试环境的访问结果，不代表所有地区和运营商都稳定可达。

## 维护

以 CONTENT-GUIDE.md 为准：content/posts/*.md 用于写博客；content/*.json 用于收藏；content/home-zh.html 与 home-en.html 用于主页。提交后自动生成并发布 docs。生成页不应单独编辑。draft 阻止网站发布，但公开仓库的源文件仍然可见。

## 账号与资料

用户名和站点已由原名称迁移到 wangshuoxuan；请分享新网址。公开姓名为王烁瑄 / Wangshuoxuan，邮箱为 2400012712@stu.pku.edu.cn，均经本人确认或授权。学位、年份、论文、奖项及具体研究结果仍待本人提供。
