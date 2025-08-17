# AI Music Environment Setup (Windows)

This guide helps you set up a Windows environment for `audiocraft`, using `pyenv-win` to manage Python versions and virtual environments, and run your main program `lilscript.py`.

---

## 1. Install pyenv-win

1. Open PowerShell (normal user, not admin).
2. Clone pyenv-win:

```powershell
git clone https://github.com/pyenv-win/pyenv-win.git $HOME\.pyenv
```

3. Create your PowerShell profile if it doesn't exist:

```powershell
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}
```

4. Open the profile in Notepad:

```powershell
notepad $PROFILE
```

5. Add these lines to the end of the file:

```powershell
# Pyenv-win setup
$env:PYENV="$HOME\.pyenv\pyenv-win"
$env:PATH="$env:PYENV\bin;$env:PYENV\shims;$env:PATH"
```

6. Save and close Notepad.
7. Apply changes immediately:

```powershell
. $PROFILE
```

8. Verify pyenv installation:

```powershell
pyenv --version
```

---

## 2. Install a Specific Python Version

1. List available Python versions:

```powershell
pyenv install --list
```

2. Install a version (example: 3.11.7):

```powershell
pyenv install 3.11.7
```

3. Set it for the current session:

```powershell
pyenv shell 3.11.7
```

4. Verify Python version:

```powershell
python --version
```

---

## 3. Create a Virtual Environment

1. Navigate to your project folder:

```powershell
cd C:\Users\richa\dev
```

2. Create a virtual environment:

```powershell
python -m venv ai_music_env
```

3. Activate it:

```powershell
.\ai_music_env\Scripts\Activate.ps1
```

4. Confirm Python version inside the venv:

```powershell
python --version
```

---

## 4. Install Dependencies

Install compatible versions of the packages:

```powershell
pip install cymem==2.0.11 preshed==3.0.10 murmurhash==1.0.13 thinc==8.3.6 blis==0.7.11
```

> Note: `thinc 8.2.5` may not exist for Windows/Python 3.11+. Use the latest compatible `8.3.x`.

Then install `audiocraft` (latest available version):

```powershell
pip install audiocraft==1.3.0
```

---

## 5. Verify Installation

```powershell
python -c "import audiocraft; print(audiocraft.__version__)"
```

You should see the installed version printed.

---

## 6. Run Your Main Program

To run your main script `lilscript.py`:

```powershell
python lilscript.py
```

Make sure you are in the project directory and the virtual environment is activated.

---

## 7. Tips

- Always activate the virtual environment before running your project.
- Use `pyenv shell <version>` to switch Python versions.
- Update `pip` if you encounter installation issues:

```powershell
python -m pip install --upgrade pip
```

