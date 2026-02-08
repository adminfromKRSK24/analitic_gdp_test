# analitic_gdp_test

```bash
    # Перед первым запуском
    
    # Перейти в проект, создать и активировать окружение
    python3 -m venv venv
    source venv/bin/activate
    
#    Установить зависимости
    pip install < requirements.txt
    # Запуск скрипта
    python3 main.py --files economic1.csv economic2.csv --report "average-gdp"
    
#    Запуск тестов
    python3 -m pytest test_parser.py -v
    
#    Посмотреть покрытие
    python3 -m pytest --cov . --cov-report=term-missing
```