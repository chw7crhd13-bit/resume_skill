# Resume Profile Schema

The saved profile is JSON. Keep fields stable and append evidence instead of replacing it.

```json
{
  "basics": {
    "name": "",
    "email": "",
    "phone": "",
    "links": [],
    "target_roles": [],
    "target_locations": [],
    "languages": []
  },
  "education": [
    {
      "school": "",
      "degree": "",
      "major": "",
      "start": "",
      "end": "",
      "gpa": "",
      "rank": "",
      "courses": []
    }
  ],
  "experience": [
    {
      "organization": "",
      "role": "",
      "type": "internship|work|campus|volunteer",
      "start": "",
      "end": "",
      "bullets": [],
      "tools": [],
      "metrics": [],
      "source_notes": ""
    }
  ],
  "projects": [
    {
      "name": "",
      "role": "",
      "start": "",
      "end": "",
      "description": "",
      "bullets": [],
      "tools": [],
      "links": []
    }
  ],
  "awards": [
    {
      "name": "",
      "issuer": "",
      "date": "",
      "level": "",
      "selection_rate": ""
    }
  ],
  "skills": {
    "technical": [],
    "domain": [],
    "tools": [],
    "certifications": []
  },
  "preferences": {
    "language": "zh|en|auto",
    "length": "one-page|two-page|auto",
    "redactions": []
  }
}
```

Merge policy:

- Preserve the original wording in `source_notes` when parsing rough notes.
- Deduplicate by organization + role + date for experience, and by project/award name for projects and awards.
- Prefer later, more complete values for empty scalar fields.
- Do not delete older bullets unless the user asks.

