# Основное приложение

Приложение реализует следующее API:

* GET /info - возвращает всю информацию о ноде из Metadata API в формате JSON
* GET /load - произвольный метод выполняющий вычислительные операции способные нагрузить CPU ноды. 
Нужно учесть время исполнения этого метода - он не должен быть долгим, соединение не должно завершаться по таймауту.
Один вызов этого метода нагружает все ядра ноды на 100. Время нагрузки задаётся через опциональный параметр timeout и по умолчанию составляет 15 секунд.
Пример использования: /load?timeout=300 - нагружает все ядра ноды на 5 минут.


## Инструкция по деплою приложения.

1. В консоль управления облаком импортировать публичный SSH-ключ, если это не было сделано раньше.
2. В группах безопасности открыть входящие TCP порты как минимум: 22, 5000
3. Создать Elastic-IP. Он нужен буден временно для первоначальной настройки сервера.
4. Создать новый экземпляр виртуальной машины Ubuntu 22.04 [Cloud Image]
Тип машины: m5.large
Тег Name: cpu bound
Количество экземпляров: 1
Elastic IP: выбрать автоматически
5. Залогиниться по внешнему IP адресу по SSH используя импортированный ключ и имя пользователя ec2-user.
6. Выполнить: sudo apt update
7. Поставить пакеты python3-venv и python3-pip: sudo apt install python3-venv и python3-pip
8. Создать каталог ~/dev/croc: mkdir -p ~/dev/croc
9. Перейти в каталог ~/dev/croc и склонировать этот репозиторий: git clone git@github.com:CrocBomber/start_task_cpu_bound_app.git
10. Перейти в каталог со склонированым репозиторием: cd start_task_cpu_bound_app
11. Создать виртуальное окружение командой: python3 -m venv .venv
12. Активировать виртуальное окружение командой: . .venv/bin/activate
13. Установить зависимости командой: pip install -r requirements.txt
14. Скопировать файл template.uwsgi.ini в текущий каталог с новым именем uwsgi.ini: cp template.uwsgi.ini uwsgi.ini
15. Отредактировать файл uwsgi.ini поменяв в параметре chdir подстроку %APP_DIR% на /home/ec2-user/dev/croc/start_task_cpu_bound_app
16. Скопировать файл template.uwsgi.service в текущий каталог с новым именем uwsgi.service: cp template.uwsgi.service uwsgi.service
17. Отредактировать файл uwsgi.service поменяв в параметре ExecStart подстроку %UWSGI_PATH% на /home/ec2-user/dev/croc/start_task_cpu_bound_app/.venv/bin/uwsgi
и подстроку %APP_DIR% на /home/ec2-user/dev/croc/start_task_cpu_bound_app
Общий вид параметра ExecStart должен получиться:
ExecStart=/home/ec2-user/dev/croc/start_task_cpu_bound_app/.venv/bin/uwsgi --ini /home/ec2-user/dev/croc/start_task_cpu_bound_app/uwsgi.ini
18. Добавить службу в systemd командой: sudo ln -s /home/ec2-user/dev/croc/start_task_cpu_bound_app/uwsgi.service /etc/systemd/system/uwsgi.service
19. Активировать службу командой: sudo systemctl enable uwsgi.service
20. Запустить службу командой: sudo systemctl start uwsgi.service 
21. Проверить статус службы, что нет ошибок: sudo systemctl status uwsgi.service
22. Проверить результат обращения на сервис /info по порту 5000, например: http://217.73.60.18:5000/info
23. Для дополнительной проверки можно перезагрузить виртуальную машину через консоль управления облаком и убедиться, что после перезапуска сервис снова будет работать.
24. Для дальнейшего создания эталонного образа машины необходимо выключить машину через консоль управления облаком.
25. Сделать новый снимок жесткого диска машины, тег Name для снимка задать cpu bound.
26. Создать новый образ с именем cpu bound используя снимок созданный на предыдущем шаге.
При создании образа установить в значение "Нет" флаг "Удалить с экземпляром".
27. Создать новый шаблон запуска выбрав образ cpu bound созданный на предыдущем шаге.
Тип машины: m5.large
Имя шаблона запуска: cpu_bound
Поставить галочку: Удалить в случае выключения
