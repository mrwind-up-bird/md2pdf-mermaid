# macOS Setup Guide for md2pdf-mermaid

This guide provides detailed instructions for installing and using md2pdf-mermaid on macOS.

## Table of Contents

- [Why Virtual Environment is Required](#why-virtual-environment-is-required)
- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

---

## Why Virtual Environment is Required

macOS (specifically macOS with Homebrew Python or Python 3.11+) uses **externally-managed Python environments** (PEP 668). This means you cannot install packages directly to the system Python without using a virtual environment.

**Benefits of using a virtual environment:**
- Isolated dependencies per project
- No conflicts with system packages
- Easy cleanup (just delete the venv folder)
- No need for sudo/administrator privileges

---

## Quick Start

```bash
# 1. Navigate to your project directory
cd /path/to/your/project

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install md2pdf-mermaid
pip install md2pdf-mermaid

# 5. Install Playwright browser
playwright install chromium

# 6. Convert your markdown files
md2pdf document.md
```

**That's it!** You're ready to convert Markdown to PDF.

---

## Detailed Installation

### Prerequisites

- **macOS 11.0 (Big Sur) or later** (recommended)
- **Python 3.8+** (check with `python3 --version`)
- **130 MB free space** for Chromium browser
- **Internet connection** for downloading dependencies

### Step 1: Install Python (if needed)

macOS comes with Python, but you may want a newer version:

```bash
# Check current Python version
python3 --version

# If you need to install/upgrade Python, use Homebrew
brew install python@3.12
```

### Step 2: Create Virtual Environment

```bash
# Navigate to your project directory
cd /path/to/your/project

# Create a virtual environment named 'venv'
python3 -m venv venv
```

This creates a `venv` folder in your current directory.

### Step 3: Activate Virtual Environment

```bash
# Activate the virtual environment
source venv/bin/activate
```

You'll see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

### Step 4: Install md2pdf-mermaid

```bash
# Install from PyPI (recommended)
pip install md2pdf-mermaid

# Or install from GitHub (latest development version)
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
```

### Step 5: Install Playwright Browser

```bash
# Install Chromium browser (required for rendering)
playwright install chromium
```

This downloads ~130 MB of Chromium browser to `~/Library/Caches/ms-playwright/`.

### Step 6: Verify Installation

```bash
# Check md2pdf is installed
md2pdf --version

# Check Python can import the module
python -c "import md2pdf; print('md2pdf installed successfully!')"
```

---

## Usage

### Basic Usage

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Convert markdown to PDF
md2pdf document.md

# Custom output filename
md2pdf document.md -o report.pdf

# With custom title
md2pdf document.md --title "My Report"
```

### Advanced Usage

```bash
# Letter page size (instead of A4)
md2pdf document.md --page-size letter

# Landscape orientation
md2pdf document.md --orientation landscape

# High-quality Mermaid diagrams
md2pdf document.md --mermaid-scale 3 --mermaid-theme forest

# Disable Mermaid rendering (faster)
md2pdf document.md --no-mermaid

# Use legacy ReportLab engine (no emoji)
md2pdf document.md --engine reportlab --emoji-strategy remove
```

### Batch Conversion

Convert multiple files:

```bash
# Activate virtual environment
source venv/bin/activate

# Convert all markdown files in current directory
for file in *.md; do
    md2pdf "$file" -o "${file%.md}.pdf"
done
```

### Deactivating Virtual Environment

When you're done:

```bash
deactivate
```

This returns you to the system Python environment.

---

## Troubleshooting

### Error: "externally-managed-environment"

**Symptom:**
```
error: externally-managed-environment
```

**Solution:**
You're trying to install without a virtual environment. Follow the installation steps above.

### Error: "No module named 'md2pdf'"

**Symptom:**
```
ModuleNotFoundError: No module named 'md2pdf'
```

**Solution:**
Activate the virtual environment first:
```bash
source venv/bin/activate
md2pdf document.md
```

### Error: "command not found: md2pdf"

**Symptom:**
```
zsh: command not found: md2pdf
```

**Solution:**
The virtual environment is not activated:
```bash
source venv/bin/activate
md2pdf document.md
```

### Error: "Playwright not found"

**Symptom:**
```
ModuleNotFoundError: No module named 'playwright'
```

**Solution:**
Install Playwright:
```bash
source venv/bin/activate
pip install playwright
playwright install chromium
```

### Mermaid Diagrams Not Rendering

**Symptom:**
Mermaid code blocks appear as text in the PDF.

**Solution:**
1. Check Playwright is installed:
   ```bash
   source venv/bin/activate
   python -c "import playwright; print('Playwright installed!')"
   ```

2. Reinstall Chromium:
   ```bash
   playwright install --force chromium
   ```

3. Test with a simple diagram:
   ```bash
   echo '```mermaid
   graph LR
       A --> B
   ```' > test.md
   md2pdf test.md
   ```

### Permission Issues

If you get permission errors, never use `sudo` with pip in a virtual environment. Instead:

1. Deactivate current environment: `deactivate`
2. Delete the venv: `rm -rf venv`
3. Create fresh environment: `python3 -m venv venv`
4. Activate and reinstall: `source venv/bin/activate && pip install md2pdf-mermaid`

---

## Uninstallation

### Remove Package Only

```bash
# Activate virtual environment
source venv/bin/activate

# Uninstall md2pdf-mermaid
pip uninstall md2pdf-mermaid
```

### Remove Everything

```bash
# Deactivate virtual environment (if active)
deactivate

# Remove virtual environment
rm -rf venv

# Remove Playwright browsers (optional)
rm -rf ~/Library/Caches/ms-playwright
```

---

## Tips and Best Practices

### 1. Alias for Convenience

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias md2pdf-activate='source venv/bin/activate'
```

Then just run:
```bash
md2pdf-activate
md2pdf document.md
```

### 2. Global Virtual Environment

If you use md2pdf frequently across projects:

```bash
# Create global venv in your home directory
python3 -m venv ~/.venvs/md2pdf

# Install md2pdf
source ~/.venvs/md2pdf/bin/activate
pip install md2pdf-mermaid
playwright install chromium

# Create alias in ~/.zshrc
echo 'alias md2pdf="~/.venvs/md2pdf/bin/md2pdf"' >> ~/.zshrc
source ~/.zshrc

# Now use md2pdf from anywhere without activation
md2pdf document.md
```

### 3. VS Code Integration

If using VS Code:

1. Open Command Palette (Cmd+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose `./venv/bin/python`

VS Code will automatically activate the venv in its integrated terminal.

### 4. Update Package

```bash
source venv/bin/activate
pip install --upgrade md2pdf-mermaid
```

---

## macOS Versions Tested

- macOS 15 (Sequoia) - ✅ Working
- macOS 14 (Sonoma) - ✅ Working
- macOS 13 (Ventura) - ✅ Working
- macOS 12 (Monterey) - ✅ Working
- macOS 11 (Big Sur) - ✅ Working (minimum required)

---

## Architecture Support

- **Apple Silicon (M1/M2/M3/M4)** - ✅ Native ARM64 support
- **Intel (x86_64)** - ✅ Full support

---

## Getting Help

If you encounter issues:

1. **GitHub Issues**: https://github.com/rbutinar/md2pdf-mermaid/issues
2. **Documentation**: https://github.com/rbutinar/md2pdf-mermaid
3. Include in your report:
   - macOS version (`sw_vers`)
   - Python version (`python3 --version`)
   - Error message
   - Steps to reproduce

---

## Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [PEP 668 - Externally Managed Environments](https://peps.python.org/pep-0668/)
- [Playwright Documentation](https://playwright.dev/python/)
- [Mermaid Diagram Syntax](https://mermaid.js.org/)

---

**Happy Converting!** 🎉

If you find this tool useful, consider starring the repository on GitHub.
