# Publishing CapGenie to PyPI and GitHub

## Prerequisites

1. **PyPI Account**
   - Register on PyPI: https://pypi.org/account/register/
   - Register on TestPyPI: https://test.pypi.org/account/register/
   - Install required tools:
     ```bash
     pip install --upgrade build twine
     ```
     Or using UV (as in your original):
     ```bash
     uv add --dev build twine
     ```

2. **GitHub Account**
   - Create a new repository on GitHub (if not already done)
   - Initialize git in your project directory if not already done:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/yourusername/capgenie.git
     git push -u origin main
     ```

## Publishing to PyPI

### 1. Clean up previous builds
```bash
# Remove previous builds and dist folders
rm -rf dist/* build/*
```

### 2. Build the package
```bash
python -m build
```

## Publishing
### To Test PyPI first (recommended)
1. Create an account on Test PyPI: https://test.pypi.org/account/register/
2. Upload to Test PyPI:
```bash
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*                                                       
```
3. Enter pypi api token
   

4. Test installation:
```bash
uv pip install --index-url https://test.pypi.org/simple/ free-llm-toolbox
```

## Version Updates
1. Update version in pyproject.toml !
2. Rebuild and upload as above