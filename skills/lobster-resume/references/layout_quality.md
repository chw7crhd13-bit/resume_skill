# Layout Quality

Use this reference when generating DOCX/PDF resumes or when a user critiques resume appearance.

## Core Principle

Resume generation is iterative. A good resume is not only tailored text; it is readable typography, clear hierarchy, and controlled density.

## Output Preference

Default to an editable DOCX so the user can fine-tune wording and spacing in Word/WPS. Use `scripts/render_resume_docx.py` for a deterministic Word draft, or copy a selected bundled Word template when it clearly matches the JD style.

## PDF Renderer Preference

Use `scripts/render_resume_pdf.py` when the user asks for a final/export PDF or when visual QA requires a PDF because it uses ReportLab canvas-level control:

- trial layout before final rendering
- dynamic font scale and line height
- sidebar + main-content templates
- optional photo
- text remains extractable for ATS

Avoid final Markdown-to-PDF output except for quick drafts.

For stronger composition heuristics, also read `poster_layout_patterns.md`.

## Canva.com Platform Note

Canva.com can be useful when the user explicitly wants a design-platform template, but it is not the default resume renderer.

Use Canva only when all are true:

- The user asks for Canva/Canva.com specifically.
- Authentication and API/app permissions are available.
- A target Canva design/template is available or the user accepts creating one.
- The final export can still be reviewed for ATS readability and layout quality.

If those conditions are not met, use the default editable DOCX workflow and export PDF locally when needed.

## Visual QA Checklist

Render DOCX/PDF pages to PNG and inspect them before delivery when tooling is available:

- Page is not blank, transparent, black-background, clipped, or corrupted.
- Name and target role are visible in the first viewport.
- Sections have clear hierarchy; headings are not the same weight as body text.
- Body text is readable at normal zoom; avoid tiny dense paragraphs.
- Bullets do not collide, overflow, or wrap awkwardly.
- The strongest JD matches appear in the top third of the page.
- Sidebar, if used, does not dominate the page or waste excessive vertical space.
- One-page resumes have balanced whitespace; two-page resumes have clean section transitions.
- Text can still be selected/extracted from the PDF.

## Dynamic Density Rules

When content is too long:

1. Cut weak or off-target bullets.
2. Shorten bullets to one result-oriented line where possible.
3. Move secondary skills to sidebar.
4. Reduce body scale by small steps, not below readable size.
5. Switch to two pages only when content quality justifies it.

When content is too sparse:

1. Add a role-targeting summary.
2. Promote coursework, tools, or awards relevant to the JD.
3. Use a calmer one-column template if the sidebar looks empty.

## Style Notes

- Finance, audit, consulting, SOE: conservative one-column or restrained two-column.
- Tech, AI, product, data: clean two-column with keywords and tools visible.
- Creative, brand, media: warmer accents are acceptable, but keep ATS readability.
- Research/quant: project and methodology hierarchy matters more than decoration.
