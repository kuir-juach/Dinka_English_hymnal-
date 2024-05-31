# SDAHymnals

[![CI workflow](https://github.com/kuir-juach/Dinka_English_hymnal-/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/kuir-juach/Dinka_English_hymnal-/actions/workflows/CI.yml)
[![publish workflow](https://github.com/kuir-juach/Dinka_English_hymnal-/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/kuir-juach/Dinka_English_hymnal-/actions/workflows/publish.yml)
![lang: din](https://img.shields.io/badge/lang-din-0a0.svg?style=flat&labelColor=333)
![lang: en](https://img.shields.io/badge/lang-en-0a0.svg?style=flat&labelColor=333)
![lang: sw](https://img.shields.io/badge/lang-sw-0a0.svg?style=flat&labelColor=333)

## Development

- `pip install -r requirements.txt`

### Pre-commit

- `pre-commit install`
- Optional: `pre-commit run --all-files`

### Manually run linting

- `check-json ./hymnals/**/*.json`
- `end-of-file-fixer ./hymnals/**/*.json`
- `pretty-format-json --no-ensure-ascii ./hymnals/**/*.json`
- `trailing-whitespace-fixer --markdown-linebreak-ext=md ./hymnals/**/*.json`
- `check-jsonschema --schemafile ./json-schema.json ./hymnals/**/*.json`
