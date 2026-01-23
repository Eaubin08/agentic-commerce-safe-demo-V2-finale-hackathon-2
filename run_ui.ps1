# Script PowerShell pour lancer l'interface Streamlit
$env:PYTHONPATH = (Get-Location).Path
streamlit run ui/app.py
