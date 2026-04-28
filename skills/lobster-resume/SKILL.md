---
name: lobster-resume
description: Use this skill when the user wants to build, store, update, brainstorm, or tailor a resume/CV from candidate background information and a job description, including JD text, screenshots, PDFs, DOCX files, webpages, or copied postings. It collects schools, GPA, internships, projects, awards, skills, languages, and preferences, saves the profile, offers JD-driven brainstorming to uncover relevant experiences and skills, then generates a company- and role-matched editable Word resume by default plus interview advice.
---

# Lobster Resume

龙虾简历用于两类任务：

1. 建档：收集并保存用户的基础履历信息。
2. 定制：用户给出任意 JD（文字、截图、PDF、DOCX、网页内容等）后，先判断模板和匹配方向，再询问用户是否进入头脑风暴，最后默认生成可编辑 Word 简历与面试建议；用户需要时再导出 PDF。

This skill includes a bundled resume template library under `assets/templates/` with many Word templates and preview images across industries. Before comparing the candidate profile against the JD, mention that the skill has multiple templates and will choose one based on the JD, company style, and candidate background.

## Storage

Use `scripts/profile_store.py` to read and update the profile whenever persistence is needed.

- Default profile path: workspace-local `.lobster-resume/profile.json`.
- If the user asks for global reuse across projects, use `--path ~/.codex/lobster-resume/profile.json` and explain that this stores resume data on the local machine.
- Never store secrets such as ID numbers, full addresses, bank details, or private account tokens.
- If the user uploads new background information, merge it into the saved profile instead of overwriting unrelated fields.

Quick commands:

```bash
python3 skills/lobster-resume/scripts/profile_store.py show
python3 skills/lobster-resume/scripts/profile_store.py merge --input incoming_profile.json
python3 skills/lobster-resume/scripts/profile_store.py missing
```

## Dependencies

DOCX rendering requires `python-docx`. PDF rendering requires `reportlab`. In Codex desktop, prefer the bundled workspace Python when available because it usually already includes the document/PDF stack. If `python3` raises `ModuleNotFoundError`, install dependencies:

```bash
uv pip install python-docx reportlab pypdf
```

If `uv` is unavailable:

```bash
python3 -m pip install python-docx reportlab pypdf
```

## Build The Profile

When information is incomplete, ask only for the fields needed for the next useful resume. Prefer one compact checklist instead of many rounds.

Core fields:

- Basic: name, phone/email/LinkedIn/GitHub/portfolio, target city, target role.
- Education: school, degree, major, graduation date, GPA/rank, relevant courses.
- Internship/work: company, role, dates, business context, actions, tools, metrics, impact.
- Projects: project name, role, dates, stack/methods, measurable outcomes, links.
- Awards: award name, issuer, date, rank/level, selection rate if known.
- Skills: programming/tools, domain methods, languages, certificates.
- Preferences: Chinese/English resume, one-page/two-page, target industry, privacy redactions.

If the user provides rough notes, normalize them into structured profile JSON with evidence-preserving wording. Do not invent metrics. Use `[待补充]` for important missing facts.

## JD Intake

When a JD arrives:

1. Extract the JD text. For screenshots/images, OCR visually; for PDFs/DOCX, use the available document/PDF tooling if needed.
2. Identify company, role, industry, seniority, location, required skills, preferred skills, responsibilities, culture signals, and application language.
3. Choose a template family from the bundled catalog. Read `references/template_catalog.md` when selecting templates.
4. Read the saved profile. If none exists, collect a minimal profile first.
5. Before generating, ask whether the user wants a JD-driven brainstorming round. Explain that this can uncover hidden experiences, adjacent skills, coursework, tools, or small projects that make the resume more targeted.
6. If the user agrees, follow `references/brainstorming_guide.md`: ask focused questions, collect answers, merge useful evidence into the profile, and then generate.
7. If the user declines or asks for speed, generate the best draft from existing evidence and list missing evidence that would improve the resume.
8. Map JD requirements to candidate evidence. Prefer direct matches, then adjacent transferable evidence.
9. Generate the resume unless a missing field would materially change the result.

## Tailoring Rules

- Lead with the evidence most relevant to the JD.
- Rewrite bullets as action + scope + method/tool + measurable result.
- Mirror important JD keywords naturally for ATS, but keep claims truthful.
- Keep one-page resumes dense and scannable; cut weak or unrelated bullets first.
- Use company-appropriate tone and layout. For detailed style selection, read `references/company_style_playbook.md`.
- Use the bundled Word template library when the user wants a DOCX/Word-style resume. For template selection, read `references/template_catalog.md`.
- For JD-driven experience discovery and interview advice, read `references/brainstorming_guide.md`.
- For schema details and output contracts, read `references/resume_schema.md` when creating or patching saved profile data.
- For PDF layout decisions, read `references/layout_quality.md` and use the canvas renderer when possible.
- For stronger visual composition, read `references/poster_layout_patterns.md` and borrow poster-generator ideas such as layers, grids, visual anchors, and template variables without sacrificing ATS readability.

## Output

Default output is an editable Word document (`.docx`) plus a short Markdown note. Use PDF only when the user asks for a final/export version or a visual check. Include:

- Targeted resume.
- Short tailoring note listing the JD keywords emphasized.
- Missing facts that would improve the next version.
- Interview advice based on the final resume/JD fit: likely questions, weak spots to prepare, and suggested stories.

For DOCX generation, default to the local Word renderer unless a bundled template is clearly better.

1. Convert the tailored resume into the JSON contract expected by `scripts/render_resume_docx.py`.
2. Generate an editable DOCX:

```bash
python3 skills/lobster-resume/scripts/render_resume_docx.py --input tailored_resume.json --output output/docx/tailored_resume.docx
```

3. When possible, render-check the DOCX using the available document tooling before delivery.
4. If using a bundled Word template, copy the selected template from `assets/templates/` into the output directory and replace placeholder content while preserving styles.

For PDF generation, use the local canvas renderer. Do not use Markdown-to-PDF as the final output path unless the user only wants a rough draft.

1. Convert the tailored resume into the JSON contract expected by `scripts/render_resume_pdf.py`.
2. Generate a PDF with the canvas renderer:

```bash
python3 skills/lobster-resume/scripts/render_resume_pdf.py --input tailored_resume.json --output output/pdf/tailored_resume.pdf
```

3. Render the PDF to an image using `pdftoppm`, `sips`, or an available PDF renderer.
4. Inspect the rendered page. If typography, spacing, overflow, hierarchy, or density is weak, revise the JSON content or renderer settings and regenerate.
5. Repeat until the PDF is visually credible for the target company style.

For DOCX generation, use the relevant document tooling, render-check the final file when possible, and keep the visual style consistent with the selected company category.

If the user explicitly asks for Canva.com output, treat it as an external design-platform workflow: use Canva only when authentication, a template/design ID, and export permissions are available. Otherwise keep the default editable DOCX workflow, with the local canvas renderer available for PDF export because it is deterministic, ATS-readable, and does not depend on external accounts.

## Iterative Debugging

Treat every resume as a layout + content product, not a one-shot text artifact.

- First pass: generate the tailored content and an editable DOCX.
- Visual pass: inspect rendered pages for density, hierarchy, alignment, whitespace, clipping, and readability.
- Content pass: check that the strongest JD matches are visible in the first third of the resume.
- Adjustment pass: tune section order, bullet length, font scale, line height, sidebar width, or page count.
- Final pass: verify text extraction still works and no important claims were invented.

## Quality Bar

- No fabricated schools, employers, dates, awards, tools, certifications, or quantified impact.
- Brainstorming may transform partial familiarity into honest resume language, but never claim mastery, production use, certificates, awards, or metrics the user did not provide.
- No private data beyond what the user supplied.
- Keep Chinese resumes natural and concise; keep English resumes ATS-friendly and accomplishment-oriented.
- If the JD and profile conflict, state the mismatch and choose the truthful version.
- DOCX output is the default deliverable so the user can fine-tune wording and layout. PDF output must be visually checked after rendering; do not deliver a PDF that only "technically generated" but looks unpolished.
- Font size and spacing must adapt to content length. Prefer reducing weak content before making the page unreadably small.
