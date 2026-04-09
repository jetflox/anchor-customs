@echo off
echo ============================================
echo   Anchor Customs Chatbot - Starting...
echo ============================================
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Run the chatbot
python app.py

pause
