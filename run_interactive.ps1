# Script PowerShell pour lancer la démo interactive
$env:PYTHONPATH = (Get-Location).Path
python demo/interactive_demo.py
