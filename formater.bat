@ECHO OFF

python -m black --line-length 88 *.py
ECHO "if 'black' is not installed, install it with: 'pip install black'"

PAUSE