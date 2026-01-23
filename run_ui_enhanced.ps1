# Script PowerShell pour lancer l'interface Streamlit améliorée
$env:PYTHONPATH = (Get-Location).Path
streamlit run ui/app_enhanced.py
