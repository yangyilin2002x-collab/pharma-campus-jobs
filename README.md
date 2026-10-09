# 2027届医药秋招雷达

## 网站功能
- 招聘目录、关键词和方向筛选。
- 本地投递追踪（准备投递、已投递、面试中、已获 Offer、已结束）。
- JSON 备份导入/导出。
- GitHub Actions 定时检索公开 RSS 招聘新闻线索。

## 启用 GitHub Pages
1. 打开仓库 **Settings → Pages**。
2. 在 **Build and deployment** 将 Source 选为 **Deploy from a branch**。
3. Branch 选择 **main**，文件夹选择 **/(root)**，保存。
4. 等待 Actions/Pages 构建完成，网址通常为 `https://yangyilin2002x-collab.github.io/pharma-campus-jobs/`。

## 启用自动更新
1. 打开 **Settings → Actions → General → Workflow permissions**。
2. 选择 **Read and write permissions** 并保存。工作流需要写入更新后的 `data/jobs.json`。
3. 打开 **Actions** 标签页，进入 **Update recruitment leads**，点击 **Run workflow** 手动测试。
4. 工作流计划每 6 小时运行一次（UTC 时间的第 17 分钟）。GitHub 的计划任务可能延迟，不保证精确实时运行。

## 重要限制
- `data/jobs.json` 中的企业官方招聘入口并不代表该企业现在有开放职位。
- 自动更新脚本只检索列出的公开 Google News RSS 搜索结果，并过滤部分校招关键词。它不能覆盖所有药企或招聘网站，也无法保证捕捉全部岗位。
- 新发现的新闻被标记为“公开新闻/RSS线索（非官方岗位页）”，需要点击原文核实，再去企业官方招聘系统申请。
- 不抓取需要登录、验证码、或明确禁止自动访问的页面。
- 投递记录目前存于浏览器 localStorage；清除浏览器数据会丢失，跨设备不会同步。请使用页面上的“导出备份”保存数据。
- 本项目不是招聘方或官方招聘平台，岗位要求、开放状态和截止时间均应以企业官方页面为准。
