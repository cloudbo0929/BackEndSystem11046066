# BackEndSystem
後台與API

# 安裝套件指令
pip install -r requirements.txt

# 啟動後端
python manage.py runserver

# 啟動ASGI Server(nodeRed新增訊息成功後用來提醒的)
uvicorn BackEndSystem.asgi:application --host 0.0.0.0 --port 8000

# 載redis (協助nodered 與 ASGI 的中繼Server)
去 https://github.com/tporadowski/redis/releases 載.msi檔案