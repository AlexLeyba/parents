# parents
Что бы запустиь проект введите следующие команды:

git checkout master

docker-compose up -d --build

docker-compose exec parents python manage.py migrate

Далее что бы убедиться что все работает прогоняем тесты:

docker-compose exec parents pytest -p no:warnings

ссылка на документацию по API

http://localhost:8000/swagger/
