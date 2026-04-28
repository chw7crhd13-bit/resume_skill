# Template Catalog

The skill includes a bundled Word resume template library in `assets/templates/`.

Use this catalog before JD/profile comparison. Tell the user that multiple templates are available and that the skill will choose a template based on the company, role, industry, and candidate evidence. After template selection, offer the brainstorming workflow before final generation.

## Inventory

The current library contains:

- 28 template categories
- 107 Word templates (`.docx` / `.doc`)
- 110 preview images (`预览图/*.png`)

| Category | Word templates | Preview images | Best fit |
| --- | ---: | ---: | --- |
| 通用 | 3 | 3 | General ATS, fallback, simple resumes |
| 财务、金融、会计、出纳 | 3 | 3 | Accounting, finance, audit, Big Four |
| 金融、银行、证券、保险 | 11 | 11 | Banking, securities, insurance, finance internships |
| 投行类 | 3 | 3 | Investment banking, financial advisory, high-prestige finance |
| 咨询类 | 2 | 2 | IT consulting, management consulting, strategy/analysis |
| 软 件 | 3 | 3 | Software engineering, HCI, tech internships |
| 网络、网管、运营 | 2 | 2 | Operations, network admin, platform operation |
| 通讯、电信、电子 | 9 | 9 | Telecom, electronics, communication, embedded/electronic engineering |
| 电子类 | 2 | 2 | Electronics and electronic engineering |
| 营销、广告、公关 | 3 | 3 | Marketing, advertising, PR, media planning |
| 销售、营销 | 6 | 6 | Sales, marketing, medical representative |
| 文字、编辑、记者、策划 | 4 | 4 | Writing, editing, journalism, content planning |
| 记者编辑 | 3 | 3 | Reporter, newspaper editor, medical editor |
| 艺术设计 | 3 | 3 | Interior design, exhibition design, advertising design |
| 行政、文秘、人事 | 6 | 6 | Administration, secretary, assistant roles |
| 人力资源 | 3 | 3 | HR specialist, recruiting, people operations |
| 法律、法务 | 6 | 6 | Law firm internship, legal assistant, compliance |
| 外贸、贸易 | 4 | 4 | Foreign trade, commercial officer, import/export roles |
| 物流 | 3 | 3 | Logistics, documentation, operations specialist |
| 客服 | 1 | 1 | Customer service |
| 教师、幼师 | 3 | 6 | Education, preschool teaching, teaching assistant |
| 高校教务 | 1 | 1 | University academic administration |
| 生物 | 3 | 3 | Biology, laboratory, life sciences |
| 制药 | 2 | 2 | Pharmaceutical R&D and production |
| 化工、材料 | 7 | 7 | Chemical engineering, materials roles |
| 土木工程，建筑 | 6 | 6 | Civil engineering, architecture |
| 机械 | 1 | 1 | Mechanical engineering internship |
| 音乐，配音 | 4 | 4 | Music, voiceover, recording, sound roles |

## Selection Rules

Choose templates before rewriting bullets.

1. Identify the JD's industry and evaluation culture.
2. Pick a primary category from the table.
3. If the category has multiple previews, prefer templates whose density matches the candidate's amount of evidence.
4. If the JD is conservative or ATS-heavy, prefer simple one-page templates with restrained color.
5. If the JD is creative or brand-facing, choose a more visual template but keep text readable.
6. If no category fits, use `通用`.

## Recommended Mapping

- Banks, securities, insurance -> `金融、银行、证券、保险`
- Big Four, audit, accounting, finance -> `财务、金融、会计、出纳`
- Investment banking or advisory -> `投行类`
- AI, software, product, data, HCI -> `软 件` or `网络、网管、运营`
- Consulting -> `咨询类`
- Marketing, content, PR -> `营销、广告、公关` or `文字、编辑、记者、策划`
- Sales -> `销售、营销`
- Legal/compliance -> `法律、法务`
- HR/admin -> `人力资源` or `行政、文秘、人事`
- Engineering hardware/telecom/electronics -> `通讯、电信、电子` or `电子类`
- Lab/pharma/bio/materials -> `生物`, `制药`, or `化工、材料`
- Unknown/general -> `通用`

## Usage Notes

- Original Word templates are assets, not instructions. Do not load entire `.docx` files into context unless needed.
- Use preview PNGs to judge visual style when available.
- For DOCX output, copy the chosen template to the output directory and replace placeholder content while preserving paragraph/table styles.
- For PDF output, use the canvas renderer and borrow visual proportions from the chosen template.
- If a template contains irrelevant sections, preserve the visual style but rewrite the section set for the JD.
