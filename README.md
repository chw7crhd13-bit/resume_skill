# Lobster Resume Skill

`lobster-resume` 是一个用于“保存候选人基础履历 + 根据 JD 自动生成定制简历”的 Codex Skill。

它适合下面这类场景：

- 先让用户填写学校、GPA、实习经历、项目经历、获奖经历、技能等基础信息。
- 将这些信息保存成本地 profile，后续重复使用。
- 用户上传 JD 截图、文字、PDF、DOCX 或网页内容后，自动提取岗位要求。
- 根据公司/岗位风格选择简历表达方式和排版风格。
- 输出 Markdown 简历，或用 canvas 渲染器生成可投递 PDF。

## 目录结构

```text
.
├── .codex-plugin/plugin.json
├── skills/lobster-resume/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── scripts/
│   │   ├── profile_store.py
│   │   └── render_resume_pdf.py
│   └── references/
│       ├── company_style_playbook.md
│       ├── layout_quality.md
│       ├── poster_layout_patterns.md
│       └── resume_schema.md
└── README.md
```

## 核心能力

1. **履历建档**

   收集并保存用户的基础信息，包括：

   - 基本信息：姓名、邮箱、电话、目标岗位、目标城市
   - 教育经历：学校、专业、学历、GPA、排名、课程
   - 实习/工作经历：公司、岗位、时间、职责、成果
   - 项目经历：项目名称、角色、方法、工具、结果
   - 获奖经历：奖项、级别、时间、含金量
   - 技能：编程、数据、办公软件、语言、证书

2. **JD 解析与匹配**

   用户提供 JD 后，skill 会识别：

   - 公司与岗位
   - 行业与岗位方向
   - 必备技能和加分技能
   - 工作职责
   - 公司风格和简历风格倾向

3. **定制简历生成**

   根据 JD 重排内容优先级，强化相关经历，弱化无关内容，并自然加入 ATS 关键词。

4. **PDF 排版与迭代**

   PDF 默认使用本地 canvas 渲染器 `render_resume_pdf.py`，支持：

   - A4 页面精确排版
   - 两栏/侧栏风格
   - 动态字号和行距试排
   - 头像、关键词、技能栏
   - 文本可复制，尽量保持 ATS 友好
   - 渲染后视觉检查，再继续调参

## 使用方法

在 Codex 中可以这样调用：

```text
使用 $lobster-resume，帮我保存我的基础简历信息。

姓名：
学校：
GPA：
实习经历：
项目经历：
获奖经历：
技能：
目标岗位：
```

之后当你有 JD 时：

```text
使用 $lobster-resume，根据这份 JD 给我生成一版定制简历。

JD：
……
```

如果 JD 是截图、PDF、DOCX 或网页内容，也可以直接上传，让 Codex 先提取岗位信息。

## 下载与安装

从 GitHub 下载：

```bash
git clone https://github.com/chw7crhd13-bit/resume_skill.git
cd resume_skill
```

如果只是想把 skill 拷贝到某个 Codex/OpenClaw 工作区，可以只复制 skill 目录：

```bash
cp -R skills/lobster-resume /path/to/workspace/skills/
```

## OpenClaw 调用

OpenClaw 的默认 workspace 通常在：

```text
~/.openclaw/workspace
```

把 skill 安装到 OpenClaw workspace：

```bash
git clone https://github.com/chw7crhd13-bit/resume_skill.git
mkdir -p ~/.openclaw/workspace/skills
cp -R resume_skill/skills/lobster-resume ~/.openclaw/workspace/skills/
```

检查 OpenClaw 是否识别到 skill：

```bash
openclaw skills list
openclaw skills info lobster-resume
openclaw skills check
```

本地调用一次 agent：

```bash
openclaw agent --local --message "使用 $lobster-resume，帮我保存我的基础简历信息：学校、GPA、实习经历、项目经历、获奖经历和技能。" --json
```

根据 JD 生成定制简历：

```bash
openclaw agent --local --message "使用 $lobster-resume，根据下面 JD 生成一版定制简历，并说明匹配关键词。JD：这里粘贴岗位描述。" --json
```

如果要让 OpenClaw 访问本地 PDF、截图或 DOCX，请在 message 里写清楚文件绝对路径，例如：

```bash
openclaw agent --local --message "使用 $lobster-resume，读取 /Users/you/Downloads/resume.pdf 和 /Users/you/Downloads/jd.png，生成一版定制简历 PDF。" --json
```

注意：`openclaw agent --local` 需要你的 shell 中已经配置好模型供应商 API key。可以先运行：

```bash
openclaw status
openclaw models list
```

## 保存 Profile

默认保存位置是当前工作区：

```text
.lobster-resume/profile.json
```

查看已保存信息：

```bash
python3 skills/lobster-resume/scripts/profile_store.py show
```

检查缺失字段：

```bash
python3 skills/lobster-resume/scripts/profile_store.py missing
```

合并新的 profile JSON：

```bash
python3 skills/lobster-resume/scripts/profile_store.py merge --input incoming_profile.json
```

## 生成 PDF

先准备一份定制简历 JSON，格式参考 `skills/lobster-resume/scripts/render_resume_pdf.py` 文件头部说明。

生成 PDF：

```bash
python3 skills/lobster-resume/scripts/render_resume_pdf.py \
  --input tailored_resume.json \
  --output output/pdf/tailored_resume.pdf
```

如果有头像：

```bash
python3 skills/lobster-resume/scripts/render_resume_pdf.py \
  --input tailored_resume.json \
  --output output/pdf/tailored_resume.pdf \
  --photo path/to/photo.png
```

## 依赖

PDF 渲染需要：

```bash
uv pip install reportlab pypdf
```

如果没有 `uv`：

```bash
python3 -m pip install reportlab pypdf
```

在 Codex Desktop 环境中，也可以使用 bundled workspace Python，它通常已经包含 PDF 相关依赖。

## 设计原则

- 不编造学历、经历、日期、奖项、技能或量化结果。
- 根据 JD 强化真实匹配点，而不是硬塞关键词。
- 简历不只是文字生成，还需要排版调试。
- PDF 必须渲染检查，避免乱码、黑底、溢出、拥挤、层级混乱。
- 默认本地 canvas 渲染；Canva.com 只作为用户明确要求时的外部平台流程。

## 当前状态

这是一个早期版本，已经具备完整的基础流程：

- 保存用户履历资料
- 解析 JD 并生成定制简历
- 按公司风格选择表达方式
- 使用 canvas 渲染 PDF
- 参考海报/设计生成项目优化排版

后续可以继续扩展：

- 多模板注册表
- 更丰富的公司风格分类
- 自动评分和版面质量检测
- DOCX 导出
- Canva.com 外部模板联动
