# Share-Ready Seed Generator

Generate a minimal project repository with native steering and project-local skills for
Codex and Claude:

```bash
python seed/generate.py --output dist/engineeringmodel-seed
python seed/generate.py --check dist/engineeringmodel-seed
```

The output is a generated projection. Edit canonical steering, skill content, and seed
templates in this source repository, then regenerate. The generator does not initialize
git, create a remote repository, or publish anything.
