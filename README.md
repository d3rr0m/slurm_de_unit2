# Курс Data Engineer от slurm.io
# Unit 2. Python и терминал
После установки пакета SlurmDE появится команда `start_fetching`, которая получает данные из сервиса API `http://5.159.103.105:4000/api/v1/logs` и сохраняет в файл формата CSV. 

## Сборка пакета
Python3 должен быть уже установлен.
1. Клоинруйте проект командой и перейдите в директорию проекта
 ```bash
git clone git@gitlab.slurm.io:data_engineer_s058356/data_engineer_review.git
```
переходим в папку проекта:
```bash
cd data_engineer_review
```
2. создайте виртуальное окружение:
```bash
python -m venv venv
```
3. Активируйте только что созданное виртуальное окружение.
```bash
$ source venv/bin/activate
```
либо
```bash
venv\Scripts\activate.bat
```
4. Запустите сборку пакета командой:
```bash
$ ./python3 setup.py sdist
```
5. После сборки пакет его необходимо установить. Выполнить это можно командой:
```bash
$ python3 pip install ./dist/SlurmDE-0.0.1.tar.gz
```
## Запуск
Запуск можно выполнить командой `start_fetching`. Итоговый csv файл создан в директории запуска команды `start_fetching`
### Необязательные параметры
где url - параметр командой строки. Передавайте в нем адрес сайта для получения сокращенной ссылки или вывода кол-ва кликов по уже существующей короткой ссылке.
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
