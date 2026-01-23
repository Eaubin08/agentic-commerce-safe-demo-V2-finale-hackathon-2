# Script PowerShell pour lancer les tests automatiques
$env:PYTHONPATH = (Get-Location).Path
python demo/test_scenarios.py
