import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

try:
    import py3Dmol
    print("Successfully imported py3Dmol")
    print(f"py3Dmol version: {py3Dmol.__version__}")
except ImportError as e:
    print(f"Failed to import py3Dmol: {e}")
    print("Installed packages:")
    import pkg_resources
    installed_packages = [d for d in pkg_resources.working_set]
    for package in installed_packages:
        print(f"{package.key} - {package.version}")
