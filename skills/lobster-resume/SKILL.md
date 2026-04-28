---
name: lobster-resume
description: Use this skill when the user wants to build, store, update, or tailor a resume/CV from candidate background information and a job description, including JD text, screenshots, PDFs, DOCX files, webpages, or copied postings. It collects schools, GPA, internships, projects, awards, skills, languages, and preferences, saves the profile, then generates a company- and role-matched resume style.
---

# Lobster Resume

龙虾简历用于两类任务：

1. 建档：收集并保存用户的基础履历信息。
2. 定制：用户给出任意 JD（文字、截图、PDF、DOCX、网页内容等）后，马上生成一份匹配岗位和公司风格的简历。

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

PDF rendering requires `reportlab`. In Codex desktop, prefer the bundled workspace Python when available because it usually already includes the PDF stack. If `python3` raises `ModuleNotFoundError: reportlab`, install dependencies:

```bash
uv pip install reportlab pypdf
```

If `uv` is unavailable:

```bash
python3 -m pip install reportlab pypdf
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
3. Read the saved profile. If none exists, collect a minimal profile first.
4. Map JD requirements to candidate evidence. Prefer direct matches, then adjacent transferable evidence.
5. Generate the resume immediately unless a missing field would materially change the result.

## Tailoring Rules

- Lead with the evidence most relevant to the JD.
- Rewrite bullets as action + scope + method/tool + measurable result.
- Mirror important JD keywords naturally for ATS, but keep claims truthful.
- Keep one-page resumes dense and scannable; cut weak or unrelated bullets first.
- Use company-appropriate tone and layout. For detailed style selection, read `references/company_style_playbook.md`.
- For schema details and output contracts, read `references/resume_schema.md` when creating or patching saved profile data.
- For PDF layout decisions, read `references/layout_quality.md` and use the canvas renderer when possible.

## Output

Default output is Markdown unless the user requests DOCX/PDF. Include:

- Targeted resume.
- Short tailoring note listing the JD keywords emphasized.
- Missing facts that would improve the next version.

For PDF generation, default to the local canvas renderer. Do not use Markdown-to-PDF as the final output path unless the user only wants a rough draft.

1. Convert the tailored resume into the JSON contract expected by `scripts/render_resume_pdf.py`.
2. Generate a PDF with the canvas renderer:

```bash
python3 skills/lobster-resume/scripts/render_resume_pdf.py --input tailored_resume.json --output output/pdf/tailored_resume.pdf
```

3. Render the PDF to an image using `pdftoppm`, `sips`, or an available PDF renderer.
4. Inspect the rendered page. If typography, spacing, overflow, hierarchy, or density is weak, revise the JSON content or renderer settings and regenerate.
5. Repeat until the PDF is visually credible for the target company style.

For DOCX generation, use the relevant document tooling, render-check the final file, and keep the visual style consistent with the selected company category.

If the user explicitly asks for Canva.com output, treat it as an external design-platform workflow: use Canva only when authentication, a template/design ID, and export permissions are available. Otherwise keep the default local canvas renderer because it is deterministic, ATS-readable, and does not depend on external accounts.

## Iterative Debugging

Treat every resume as a layout + content product, not a one-shot text artifact.

- First pass: generate the tailored content and a PDF.
- Visual pass: inspect rendered pages for density, hierarchy, alignment, whitespace, clipping, and readability.
- Content pass: check that the strongest JD matches are visible in the first third of the resume.
- Adjustment pass: tune section order, bullet length, font scale, line height, sidebar width, or page count.
- Final pass: verify text extraction still works and no important claims were invented.

## Quality Bar

- No fabricated schools, employers, dates, awards, tools, certifications, or quantified impact.
- No private data beyond what the user supplied.
- Keep Chinese resumes natural and concise; keep English resumes ATS-friendly and accomplishment-oriented.
- If the JD and profile conflict, state the mismatch and choose the truthful version.
- PDF output must be visually checked after rendering; do not deliver a PDF that only "technically generated" but looks unpolished.
- Font size and spacing must adapt to content length. Prefer reducing weak content before making the page unreadably small.
