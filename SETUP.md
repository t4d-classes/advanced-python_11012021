# Python Class

## Initial Project Setup

1. Ensure the right Python version is being used with `pyenv`

```pwsh
pyenv versions
```

1. Create a new virtual environment.

```pwsh
python -m venv venv
```

If prompted by VS Code to use the new virtual environment, click 'Yes'.


1. Activate the new Python environment for the current terminal session.

```pwsh
.\venv\Scripts\Activate.ps1
```

1. Verify the path of the current Python interpreter.

```pwsh
Get-Command python | Format-List -Property Path
```

1. Upgrade PIP

```pwsh
python -m pip install --upgrade pip
```

1. Install coding PIP packages. These packages will work with the Python extension to provide linting and formatting.

```pwsh
python -m pip install autopep8 mypy pylint
```

1. Freeze the packages installed to a requirements file to ease installation in the future.

```pwsh
python -m pip freeze > requirements.txt
```

1. Create `.gitignore` file.

```
.DS_Store
__pycache__
venv
*.pyc
.mypy_cache
```

1. Create a VS Code `settings.json` file for the project.

```
{
    "python.pythonPath": "venv\\Scripts\\python.exe",
    "editor.detectIndentation": false,
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "files.autoSave": "afterDelay",
    "python.languageServer": "Pylance",
    "editor.rulers": [
     79
    ],
    "python.formatting.autopep8Args": [
        "--aggressive"
    ],
    "python.linting.mypyArgs": [
        "--ignore-missing-imports",
        "--follow-imports=silent",
        "--show-column-numbers",
        "--strict"
    ],
    "python.linting.mypyEnabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--max-line-length=79",
        "--unsafe-load-any-extension=y",
        "--ignore=.git,venv,.vscode,__pycache__"
    ],
    "python.linting.pylintUseMinimalCheckers": false,
}
```

1. Create a new folder named `src/rate_demos`, and change into the folder.

```pwsh
mkdir -p src/rate_demos

cd app
```

1. Create a new, empty file named `__init__.py` in the `src` folder.

1. Create a new file named `__main__.py` and copy the following code into it.

```python
""" hello world app """

if __name__ == "__main__":
    print("Hello, World!")
```

1. From the `src` folder of the project, run the app with the following command:

```python
python -m rate_demos
```

It should output:

```pwsh
Hello, World!
```
