# order_project
 
1) Установите зависимости из файла requirements.txt с помощью pip:
   pip install -r requirements.txt
2) Установите redis
3) Запуск celery
   celery -A order_project worker -l info
4) Документация url
   http://127.0.0.1:8000/swagger/