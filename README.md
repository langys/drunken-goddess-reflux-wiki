# Next.js 站点模板

这套模板是 `game-wiki-site-builder` 技能的可执行部分。它逆向自一个真实在跑的站群（219 个域名、统一模板），用于在 3–4 小时内铺出一个新的游戏攻略 WIKI 站。

**不要手动复制这个目录。** 用脚手架脚本，它会同时替换域名、站名和包名：

```bash
cd <skill-dir>
./scripts/scaffold_site.sh ~/sites/mygame www.mygame.quest "MyGame" mygame-quest
```

---

## 技术栈

| 项目 | 选择 | 理由 |
| --- | --- | --- |
| 框架 | Next.js 15 App Router | 实测生产站用的是 **15.5.9**（从 `window.next` 字面量确认），本模板对齐该大版本 |
| 国际化 | next-intl 3，`localePrefix: 'as-needed'` | 默认语种不带前缀（`/guide`），与生产站 URL 形态一致 |
| 样式 | Tailwind 3 + HSL CSS 变量（shadcn 风格） | 设计令牌直接取自生产站构建产物 |
| 字体 | Geist / Geist Mono | 与生产站一致，`next/font` 自动内联 |
| 内容 | markdown + gray-matter frontmatter | AI 直接写 markdown 比改 TS 数据结构更省 token、更少出错 |
| 广告 | Adsterra 7 版位 + AdSense 惰性挂载 | 双轨策略：Adsterra 是唯一实际渲染的网络，AdSense 只做所有权声明 |
| 部署 | Vercel + Cloudflare DNS | 与生产站一致 |

## 已验证行为

本模板经过实际构建与运行时验证，不是"看起来能跑"：

- `tsc --noEmit` 零错误，`next build` 零报错
- 单语种（仅 en）与双语种（en + es）两种配置都能正确构建
- hub 页、spoke 页、四个法务页、`/search` 全部返回 200；未知 slug 返回 404
- 每个页面输出 `robots` + `googlebot` meta、canonical、完整 hreflang（en + 各语种 + x-default）
- 内页输出 `Article` + `BreadcrumbList` JSON-LD，首页输出 `WebSite` + `Organization` + `VideoGame`
- `sitemap.xml` 含 hub、spoke、**法务页**与 hreflang alternates，且**只列出真的有内容的语种**
- `/ads.txt`、`/robots.txt`、`/sitemap.xml`、`/search-index.json` 均可访问
- `/en/...` 会 308 归一化到 `/...`；`www`/非 `www` 会归一到配置的 host
- 暗色主题在首屏渲染前应用（无白闪）；搜索索引覆盖全部页面含法务页

用 `../scripts/verify_site.py <url>` 可在部署后复跑这套检查。

---

## 自带功能

铺开即用，不需要从零实现：

| 功能 | 位置 | 说明 |
| --- | --- | --- |
| **暗黑模式** | `components/ThemeProvider.tsx`、`ThemeToggle.tsx` | 亮/暗/跟随系统三态；`<head>` 里的同步脚本防止刷新白闪 |
| **多语言切换** | `components/LocaleSwitcher.tsx` | 下拉菜单，**保留当前页路径**；只列出真的有内容的语种 |
| **全局搜索** | `components/SearchDialog.tsx` + `scripts/build_search_index.py` | ⌘K / Ctrl+K 唤起；索引构建时生成，首次打开才加载 |
| **法务与信任页** | `content/legal/*.md` + `app/[locale]/{about,contact,privacy,terms}/` | 支持按语种覆盖，缺失时回退英文而不是 404 |
| **版权与非官方声明** | `components/SiteFooter.tsx` | 版权行 + 商标归属 + "非官方"免责 |
| **移动端导航** | `components/SiteHeader.tsx` | `<details>` 汉堡菜单，无客户端状态 |

联系邮箱来自 `config/site.config.ts` 的 `contactEmail`（`content/legal/contact.md` 用 `{{contactEmail}}` 引用）。多站共用一个邮箱时只改这一处。

---

## 铺开后的 8 步

1. **`npm install`**
2. **改 `config/site.config.ts`**：`name` / `fullName` / `title` / `description` / `tagline` / `themeColor` / `heroImage` / `twitter` / `hubs` / `ads`。
   这是唯一的身份来源——**不要在组件里硬编码游戏名**。
3. **写内容**：`content/en/<slug>.md`，格式见 `../references/03-content-engine.md`。
   同时用 `scripts/harvest_keywords.py` 生成 `config/pages.ts`。
4. **确认联系邮箱**：`config/site.config.ts` 的 `contactEmail`（默认已设为可用地址）。
5. **`npm run build`**：必须零报错。
6. **建仓库并推送**：GitHub private repo。
7. **Vercel 部署**：import 仓库，填环境变量（见 `.env.example`），Deploy。
8. **Cloudflare DNS + GSC 收录**：完整清单见 `../references/04-launch-and-indexing.md`。

---

## 目录导览

```
app/[locale]/layout.tsx          语言布局：主题初始化脚本、AdSense 挂载、Header/Footer、侧翼广告
app/[locale]/page.tsx            首页
app/[locale]/[...slug]/page.tsx  hub 页 + spoke 页（catch-all，见 references/07 第 4 节）
app/[locale]/{about,contact,privacy,terms}/   法务与信任页
app/[locale]/search/page.tsx     搜索落地页（noindex）
app/sitemap.ts | robots.ts | ads.txt/route.ts   三个 SEO 端点
components/ads/                  7 个版位 + 懒加载 + 串行队列
components/seo/                  JSON-LD 与面包屑
components/Theme*.tsx            暗黑模式（三态 + 防白闪）
components/{LocaleSwitcher,SearchDialog}.tsx    语言切换与全局搜索
config/site.config.ts            ★ 站点身份唯一来源
content/<locale>/*.md            ★ 内容
content/legal/*.md               法务页（可用 legal/<locale>/ 覆盖）
messages/*.json                  UI 文案（新增语种时复制）
scripts/build_search_index.py    构建搜索索引（build 时自动运行）
```

---

## 环境变量

见 `.env.example`。最小可用集：

```bash
NEXT_PUBLIC_SITE_URL="https://www.example-wiki.wiki"
NEXT_PUBLIC_ADSENSE_PUB_ID="pub-XXXXXXXXXXXXXXXX"
NEXT_PUBLIC_ADSTERRA_PL=""      # 原生广告子账户号，用不到可留空
```

GA4 和 Clarity 默认**不加载**——两者都会拖慢 LCP，而 GSC 已经能提供排名与曝光数据。确实需要时用 `next/script` 的 `strategy="lazyOnload"`。

---

## 建站与运营工具

项目里自带这几个脚本（`../scripts/` 是同一份源码，另有 `scaffold_site.sh` 等全流程脚本）：

| 脚本 | 用途 |
| --- | --- |
| `scripts/build_search_index.py` | 构建搜索索引（`npm run build` 自动运行） |
| `scripts/fetch_steam_media.py` | 抓官方预告片与截图进 `site.config.ts` 的 `media` 块 |
| `scripts/make_logo.py` | 从同一图形生成 SVG、32/96px PNG、16/32/48px ICO 与 Apple 图标；`npm run test:favicons` 检查格式及并行生成 |
| `scripts/fetch_trends.py` | 用 pytrends 取 Google Trends，输出做/不做的判断 |

```bash
python3 scripts/fetch_trends.py "Witchbrook" --geo US --out research/trends.json
python3 scripts/fetch_steam_media.py --appid 1846700 --site-dir .
python3 scripts/make_logo.py --name "Witchbrook" --color "#6d348c"
```

上线后与运营阶段用：`chrome-devtools-mcp`（看 SERP、验证页面）、`search-console-mcp`（GSC/Bing/GA4 查询与提交）、`search-analytics-api`（周期快照）、`adsense-site-auditor`（提交 AdSense 前合规体检）。完整映射见 `../references/08-toolchain.md`。

## 常用命令

```bash
npm run dev         # 本地开发
npm run build       # 构建（部署前必须通过）
npm run typecheck   # tsc --noEmit
npm run start       # 本地跑生产构建
```

上线后自检：

```bash
python3 ../scripts/verify_site.py https://www.example-wiki.wiki --locales en \
        --expect-adsense ca-pub-XXXXXXXXXXXXXXXX
```

---

## 三个不要动的地方

1. **`lib/adsterra.ts` 的可见度/宽度检查和同页 key 注册表**：隐藏/放不下的固定横幅不请求；重复组件、锚点和持久位导航不重复加载。
2. **共享 Banner Promise 队列**：每次赋值 `window.atOptions` 后等待脚本 load/error，不能用超时放行迟到脚本。
3. **广告容器的 `minHeight` / `width`**：空素材也保留空间；Native 自然增高，不裁切。

配置 `ads.adsterra.scriptUrls[key]` 为本站对应格式的完整入口：Banner 用 `https://bauval.org/22/<key>`，Native 用 `https://bauval.org/21/<key>`，不追加 `/invoke.js`。key 与 Native 容器 ID仍从本站 Get Code 获取；Native 与文末300×250使用各自独立 key。构建执行每页 key 检查，专项测试为 `npm run test:ads`。

Native 的 `container-<key>` 在 JSX/HTML 中提前生成，懒加载只延迟脚本。不要在 usePathname 更新时清空或重建 host；页面需要新实例时传含 locale 的页面 key。当前 SDK 自带文档级 key 去重及路由填充，重复 invoke.js 不能弥补缺失目标。build 会检查 Native 目标存在且唯一；切页验收须包含真实创意、连续导航和后退/前进。

细节与原因见 `../references/05-monetization.md`。
