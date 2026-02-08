# analitic_gdp_test


![run](./run.gif)

```bash
    # склонировать проект 
    git clone git@github.com:adminfromKRSK24/analitic_gdp_test.git
    # Перейти в директорию
    cd analitic_gdp_test
    # Перейти в проект, создать и активировать окружение
    python3 -m venv venv
    source venv/bin/activate
    
#    Установить зависимости
    pip install -r requirements.txt
    # Запуск скрипта
    python3 main.py --files economic1.csv economic2.csv --report "average-gdp"
    
#    Запуск тестов
    python3 -m pytest test_parser.py -v
    
#    Посмотреть покрытие
    python3 -m pytest --cov . --cov-report=term-missing
```