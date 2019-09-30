# HSE Lyceum Bot

VK-бот Лицея НИУ ВШЭ <br> 
<strong>Разработчики</strong>: Денисов Степан и Мелёхин Никита

## Установка и запуск

1. Склонировать репозиторий
    ```
    git clone <ссылка>
    ```
    
2. Внутри локального репозитория создать виртуальное окружение и активировать его
    ```
    virtualenv --python=python3 venv
    source venv/bin/activate
    ```

3. Установить зависимости
    ```
    pip install -r requirements.txt
    ```

4. Создать таблицы в БД
    ```
    python3 migrate.py
    ```

5. Запустить бота
    ```
    python3 main.py
    ```