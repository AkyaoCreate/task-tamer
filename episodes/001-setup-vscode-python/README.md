# 001 VS Code and Python Setup

Goal
Set up Python and Visual Studio Code correctly on Windows, macOS, or Linux, then run your first script.

Chapters
00:00 What you will get
00:25 Install Python Windows macOS Linux
02:40 Check PATH and versions
03:20 Install Visual Studio Code
04:10 Install the Python extension and select interpreter
05:00 Create a virtual environment
06:10 Create and run your first script
08:00 Optional format and lint
09:15 Troubleshooting
09:50 Next steps

Windows quick start PowerShell
```powershell
python --version
# If this opens the Microsoft Store, use:
py --version

# Create project folder and open in VS Code
mkdir C:\code\task-tamer\hello
cd C:\code\task-tamer\hello
code .

# Create venv and activate
py -3 -m venv .venv
. .\.venv\Scripts\Activate.ps1

# Upgrade pip, then run the sample
python -m pip install --upgrade pip
python hello.py
python verify_env.py
```

macOS and Linux quick start
```bash
python3 --version
mkdir -p ~/code/task-tamer/hello
cd ~/code/task-tamer/hello
code .  # or open VS Code and use File - Open Folder

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python hello.py
python verify_env.py
```

Install Visual Studio Code
- Download from https://code.visualstudio.com
- Install the Python extension by Microsoft
- Optional extensions: Pylance, Black Formatter, Ruff

Select interpreter
- VS Code Command Palette Ctrl Shift P or Cmd Shift P
- Run: Python Select Interpreter
- Pick the interpreter from `.venv`

Optional format and lint
```bash
pip install black ruff
```
- Enable Format on Save in VS Code Settings
- Select Black as default formatter
- Enable Ruff extension

Troubleshooting top tips
- If activation is blocked on Windows
  Run PowerShell as your user and execute:
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  Close and reopen the terminal.

- If VS Code cannot find your interpreter
  Use Python Select Interpreter and choose the `.venv` entry for this folder.

- If `pip` installs into the wrong Python
  Activate the venv first, then check `python -c "import sys; print(sys.executable)"`

Files in this episode
- `hello.py` prints a greeting plus your Python version
- `verify_env.py` collects useful environment info
- `.vscode/settings.json` enables Black and points to the venv
