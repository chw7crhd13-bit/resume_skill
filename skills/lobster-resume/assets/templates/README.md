# Optional Template Cache

The full Word template library is not stored in the lightweight skill checkout.

Download only the categories you need:

```bash
python3 skills/lobster-resume/scripts/download_templates.py --list
python3 skills/lobster-resume/scripts/download_templates.py --category 通用
python3 skills/lobster-resume/scripts/download_templates.py --all
```

Generated/downloaded template files are local cache assets and are ignored by Git.
