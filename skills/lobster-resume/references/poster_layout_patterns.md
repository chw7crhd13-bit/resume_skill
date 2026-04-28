# Poster Layout Patterns

Use this reference when the resume looks plain, crowded, or document-like. The goal is to borrow layout discipline from poster and design-editor projects while keeping resumes ATS-readable and professionally restrained.

## Open-Source Ideas To Borrow

These projects are useful references for principles, not mandatory dependencies:

- Vercel Satori: HTML/CSS-like layout to SVG, useful for thinking in constrained boxes, font registration, dimensions, and deterministic rendering.
- Fabric/canvas design editors such as vue-fabric-editor, yft-design, and React Canvas Editor: useful for layered object models, reusable templates, guides, alignment, and editable design elements.
- CreatiPoster: useful for the idea of multi-layer, editable graphic compositions driven by structured fields.
- Python poster-generator libraries: useful for element systems, JSON/YAML templates, variables, relative positioning, grouping, and reusable poster layouts.

## Translate Poster Ideas To Resumes

Use these mappings:

- Canvas -> one A4 page with explicit dimensions.
- Layer -> background band, sidebar, section header, role row, bullet group, photo, tag group.
- Frame -> section bounding box with known width, height, and baseline.
- Visual anchor -> name block, photo, target-role headline, or JD keyword cluster.
- Template variable -> candidate name, target role, company style, keyword tags, sections, bullets.
- Guides -> fixed margins, column gutters, baseline rhythm, section divider positions.
- Density score -> estimated text height divided by available height.

## Composition Rules

- Start with a grid. Pick one of: one-column, two-column sidebar, compact dashboard, or research-forward.
- Establish one strong visual anchor in the top-left or top band; do not let every section compete.
- Use restrained accents: one main color, one light tint, one divider color.
- Prefer repeated components over ad hoc drawing: every role row, bullet group, and tag should follow the same measurements.
- Keep section rhythm predictable: heading, divider, role/date row, bullets.
- Make the first third of the resume carry the strongest JD match.
- Use whitespace as a grouping tool, not decoration.

## Template Variants

Conservative:

- One-column or very subtle two-column.
- Minimal color, strong dates, compact bullets.
- Best for banks, audit, consulting, law, SOE, manufacturing.

Tech/Product:

- Two-column with a narrow keyword/skills rail.
- Strong headline and project/experience hierarchy.
- Best for AI, data, product, SaaS, developer tools.

Creative/Brand:

- More generous heading scale and warmer accent.
- Portfolio/link block can be a visual anchor.
- Keep the main content ATS-readable.

Research/Quant:

- Method/project-forward layout.
- Methods, datasets, tools, and outcomes must be easy to scan.

## Dynamic Layout Heuristics

Before final rendering, estimate:

- Total bullet lines.
- Sidebar fill ratio.
- Main-column overflow.
- Section balance.
- Whether the strongest evidence is above the page midpoint.

Then adjust in this order:

1. Reorder sections to match the JD.
2. Move keywords/tools to the sidebar.
3. Shorten weak bullets.
4. Switch template variant.
5. Reduce type scale slightly.
6. Split to two pages only if the user and content justify it.

## Renderer Roadmap

Future renderer improvements should follow this order:

1. Template registry: `conservative`, `tech_sidebar`, `creative`, `research`.
2. Component model: `Header`, `SidebarBlock`, `TagList`, `Section`, `Entry`, `BulletGroup`.
3. Measurement pass: calculate line wraps and section heights before drawing.
4. Scoring pass: penalize overflow, excessive tiny type, empty sidebar, and weak top-third relevance.
5. Visual QA pass: render to PNG and inspect before delivery.

