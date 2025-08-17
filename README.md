# AI Music Project

This project uses [Audiocraft](https://github.com/facebookresearch/audiocraft) to generate music with AI. It is configured to run on Windows using Python 3.11 inside a virtual environment.

## Prerequisites

- Windows 10/11
- Python 3.11
- Git
- `pip` and `venv` modules (Python standard)

## Setup Instructions

### 1. Clone the repository
```powershell
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a virtual environment
```powershell
python -m venv ai_music_env
```

### 3. Activate the virtual environment
```powershell
.\ai_music_env\Scripts\Activate.ps1
```

### 4. Upgrade pip, setuptools, and wheel
```powershell
python -m pip install --upgrade pip setuptools wheel
```

### 5. Install Audiocraft
You have two options:

**Option 1: Stable version (recommended)**
```powershell
python -m pip install audiocraft==1.3.0
```

**Option 2: Alpha version (if you specifically need v1.4.0a2)**
```powershell
python -m pip install git+https://github.com/facebookresearch/audiocraft.git@v1.4.0a2
```

### 6. Install additional dependencies (if needed)
```powershell
python -m pip install numpy soundfile torch cymem==2.0.11 preshed==3.0.10 murmurhash==1.0.13 thinc==8.2.5 blis==0.7.11
```

## Usage

Once everything is installed, you can run your scripts inside the activated environment:

```powershell
python generate_music.py
```

Replace `generate_music.py` with your own script name.

## Notes

- Ensure you are using Python 3.11 inside the virtual environment.
- If you encounter build errors, make sure `pip`, `setuptools`, and `wheel` are up to date.
- On Windows, installing some pre-release packages may require a working C++ build environment.

## License

Include your project license here.
