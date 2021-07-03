# qualix-test-assignment

Выполнено по [task.md](task.md).

## Установка

Я не стал заморачиваться с контейнеризацией. 

1. Установите на машину Python 3.8+.
2. Клонируйте репозиторий `git clone https://github.com/Sunkek/qualix-test-assignment`
3. Перейдите в директорию джанги `cd jsonrpcapi`
4. Создайте виртуальное окружение Python `python -m venv venv`
5. Активируйте его `venv\Scripts\activate` (Windows)
6. Установите зависимости `pip install -r requirements.txt`
7. Запустите проект `python manage.py runserver`

## Работа

Проект открывает эндпоинт на локалхосте по адресу localhost:8000/api/v1/test. 
Запросы этого эндпоинта спровоцируют вызов метода `auth.check` по адресу https://slb.medv.ru/api/v2/ и вывод результата в JSON.

## Особенности

Если я правильно понял суть задания, мне просто нужно вызвать JRPC-метод `auth.check` в заданном API, что и происходит при открытии localhost:8000/api/v1/test.

Я вынес всё взаимодействие с JSON RPC API в отдельный класс. При необходимости можно доработать код для создания множеста подобных классов и обращения к разным API.

Стандартная библиотека ssl для проверки сертификата требует ввод расположения файлов сертификата и ключа. 
По условию задания сертификат и ключ заданы в настройках Django, поэтому мне пришлось создавать временные файлы сертификата и ключа, 
передавать их адреса в ssl и удалять после создания коннектора.

После единичного использования ssl-коннектора его event loop закрывается, а вместе с ним и event loop сессии aiohttp (да, я люблю async). 
Поэтому мне приходится проверять loop, убивать старую сессию и создавать новую при каждом запросе. Этот момент было бы неплохо переработать.