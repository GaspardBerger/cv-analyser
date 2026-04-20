@echo off
cd /d %~dp0
echo CV-Analysator wordt gestart...
echo Sluit dit venster NIET tijdens gebruik.
echo.
python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false
pause
