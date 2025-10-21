import sys, platform, subprocess

def sh(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return out.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR {e.returncode}: {e.output.strip()}"

print("Task Tamer - Environment Check")
print("-" * 40)
print("Platform:", sys.platform)
print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("pip:", sh("python -m pip --version"))
# venv check
venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.prefix != sys.base_prefix)
print("Venv active:", venv)
