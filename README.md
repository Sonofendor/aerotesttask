# Тестовое задание на позицию Data Engineer в Aero

**Здача**: написать коннектор, который раз в 12 часов будет подключаться к API https://statsapi.web.nhl.com/api/v1/teams/21/stats и выгружать данные в БД.

**Решение**
* БД Postgres 14.4 (недавно скачивал)
* ЯП Python 3.9.7 (обычно работаю в окружении анаконды), 3.10.5 (скачал отдельно чтобы шедулить)
* Библиотеки requests 2.26.0 (уже работал с ней), psycopg2 2.8.6 (первое что нагуглил)

**Шедулинг**

Пользуюсь виндой, вместо крона у меня планировщик заданий:
![image](https://user-images.githubusercontent.com/48153021/179432034-d6230158-a118-46d8-8d94-419b11a97ff2.png)
![image](https://user-images.githubusercontent.com/48153021/179432049-1c79e1c9-d016-4e3c-a14b-46211f5e60b5.png)
![image](https://user-images.githubusercontent.com/48153021/179432055-d9de9c23-c0fa-46b4-8a2f-cee208a16004.png)
![image](https://user-images.githubusercontent.com/48153021/179432071-03e2d3fb-75b7-4f09-9323-054d5e5ce087.png)
