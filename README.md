# analitic_gdp_test


![run](./run.gif)

```bash
#   Запускаем все сразу или можем по отдельности по командам ниже
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


#### 1. Клонируем репозиторий
```bash
  git clone git@github.com:adminfromKRSK24/analitic_gdp_test.git
```

#### 2. Переходим в папку проекта
```bash
  cd analitic_gdp_test
```

#### 3. Создаём виртуальное окружение
```bash
    python3 -m venv venv
```

#### 4. Активируем виртуальное окружение
```bash
    source venv/bin/activate
```

#### 5. Устанавливаем зависимости
```bash
pip install -r requirements.txt
```

#### 6. Запускаем основной скрипт (пример)
```bash
python3 main.py --files economic1.csv economic2.csv --report "average-gdp"
```

#### 7. Запуск тестов (пример)
```bash
python3 -m pytest test_parser.py -v
```

#### 8. Посмотреть покрытие (пример)
```bash
python3 -m pytest --cov . --cov-report=term-missing
```
