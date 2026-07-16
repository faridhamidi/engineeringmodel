# Share-Ready Seed Generator

Generate a minimal project repository with native steering and project-local skills for
Codex and Claude:

```bash
python seed/generate.py --output dist/engineeringmodel-seed
python seed/generate.py --verify dist/engineeringmodel-seed
python seed/generate.py --check dist/engineeringmodel-seed
```

The output is a generated projection. Edit canonical steering, skill content, and seed
templates in this source repository, then regenerate. `--verify` checks a distributed
seed against its embedded manifest without consulting this source checkout. It proves
internal consistency, not the authenticity of an unsigned manifest. `--check` compares
against current canonical sources, including their revision and clean or modified state,
so a seed from an older commit is intentionally reported as stale.

The generator rejects VCS metadata, OS files, and language cache artifacts found below
projected source trees. It does not initialize git, create a remote repository, or
publish anything.
