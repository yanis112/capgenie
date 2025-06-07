# Publishing Instructions

## Prerequisites
- Python 3.8 or higher
- `build` and `twine` packages installed
- Valid PyPI account with API token

## Setup

1. Install build tools:
   ```bash
   pip install --upgrade build twine
   ```

## Building the Package

### On Linux/macOS:
```bash
# Clean previous builds
rm -rf dist/ build/


# Build the package
python -m build
```

### On Windows (PowerShell):
```powershell
# Clean previous builds
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue

# Build the package
python -m build
```

## Publishing to PyPI

1. First, create a PyPI API token from https://pypi.org/manage/account/token/
2. Use `twine` to upload the package:

```bash
# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

When prompted for credentials:
- Username: `__token__`
- Password: Your API token (starts with `pypi-`)

## Verifying the Upload

After uploading, you can verify your package is available at:
- TestPyPI: https://test.pypi.org/project/capgenie/
- PyPI: https://pypi.org/project/capgenie/

## Installing the Published Package

```bash
# From TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps capgenie

# From PyPI (once published)
pip install capgenie
```

## Troubleshooting

- If you get authentication errors, verify your API token is correct
- Make sure you've incremented the version in `pyproject.toml` before uploading a new version
- Check PyPI for any rate limiting if you're making multiple uploads in a short time
