# tests/test_parser.py
import sys
from unittest.mock import patch
import pytest

from main import Parser, Conroller, ReportAverageGDP, FileAverageGDP  # замените на реальный импорт


@pytest.fixture
def mock_argv():
    """Фикстура для удобной подмены аргументов"""
    original_argv = sys.argv
    yield
    sys.argv = original_argv


def test_parser_correct_files_and_report(mock_argv):
    """Проверяем, что файлы и имя отчёта корректно распарсиваются"""
    test_args = [
        "script.py",
        "--files", "data1.csv", "data2.csv", "info.xlsx",
        "--report", "average-gdp"
    ]

    with patch.object(sys, 'argv', test_args):
        parser = Parser()

        files = parser.get_files()
        report = parser.get_name()

        assert files == ["data1.csv", "data2.csv", "info.xlsx"]
        assert report == "average-gdp"


def test_parser_minimal_arguments(mock_argv):
    """Минимально допустимый набор аргументов"""
    test_args = [
        "script.py",
        "--files", "one.csv",
        "--report", "simple"
    ]

    with patch.object(sys, 'argv', test_args):
        parser = Parser()
        assert parser.get_files() == ["one.csv"]
        assert parser.get_name() == "simple"


def test_parser_report_argument_is_single_value(mock_argv):
    """Проверяем, что --report берёт только одно значение"""
    test_args = [
        "script.py",
        "--files", "file1.csv",
        "--report", "trend-report"
    ]

    with patch.object(sys, 'argv', test_args):
        parser = Parser()
        assert parser.get_name() == "trend-report"


def test_missing_files_argument_raises_error(mock_argv):
    """Если не передан обязательный --files → ошибка от argparse"""
    test_args = [
        "script.py",
        "--report", "average"
    ]

    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):  # argparse выходит с кодом 2
            Parser()


def test_missing_report_argument_raises_error(mock_argv):
    """Если не передан --report → ошибка"""
    test_args = [
        "script.py",
        "--files", "data.csv"
    ]

    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            Parser()


# ───────────────────────────────────────
# Тесты для Conroller / select_report
# ───────────────────────────────────────

# def test_select_report_unknown_report(capsys, mock_argv):
#     test_args = [
#         "script.py",
#         "--files", "data1.csv", "data2.csv", "info.xlsx",
#         "--report", "average-gdp"
#     ]
#
#     with patch.object(sys, 'argv', test_args):
#         parser = Parser()
#
#         files = parser.get_files()
#         report = parser.get_name()
#
#         assert files == ["data1.csv", "data2.csv", "info.xlsx"]
#         assert report == "average-gdp"
#
#     controller = Conroller()
#
#     # Мокаем имя отчёта
#     with patch.object(controller._parser_terminal, 'get_name', return_value="unknown-report"):
#         controller.select_report()
#
#     captured = capsys.readouterr()
#     assert "Ошибка при выборе отчёта" in captured.out
#     assert "- average-gdp" in captured.out

def test_select_report_unknown_report(capsys, mocker):
    # Мокаем parser_terminal, чтобы он вернул нужные значения
    mocker.patch(
        'main.Parser.parser_terminal',
        return_value=(['fake.csv'], 'unknown-report')
    )

    controller = Conroller()  # теперь не упадёт
    controller.select_report()

    captured = capsys.readouterr()
    assert "Ошибка при выборе отчёта" in captured.out
    assert "- average-gdp" in captured.out

def test_select_report_invalid_file_extension(capsys, mocker):
    # Мокаем parser_terminal → возвращаем файлы с плохим расширением
    mocker.patch(
        'main.Parser.parser_terminal',
        return_value=(['data.txt', 'image.jpg'], 'average-gdp')
    )

    controller = Conroller()
    controller.select_report()

    captured = capsys.readouterr()
    assert "Расширение файла не CSV" in captured.out


# ────────────────────────────────────────────────────────────────
# Тест 3 — нормальный сценарий с реальными файлами
# ────────────────────────────────────────────────────────────────

def test_select_report_valid_input(tmp_path, capsys, mocker):
    # Создаём временные файлы
    file1 = tmp_path / "test1.csv"
    file2 = tmp_path / "test2.csv"

    file1.write_text("""country,gdp
USA,25000.5
Russia,1500.75
USA,26000
""")

    file2.write_text("""country,gdp
Russia,1600
China,18000
""")

    # Мокаем parser_terminal — возвращаем наши файлы и правильный отчёт
    mocker.patch(
        'main.Parser.parser_terminal',
        return_value=([str(file1), str(file2)], 'average-gdp')
    )

    controller = Conroller()
    controller.select_report()

    captured = capsys.readouterr()
    output = captured.out

    assert "average-gdp" in output
    assert "USA" in output
    assert "Russia" in output
    assert "China" in output
    # Проверяем средние значения (примерные границы)
    assert any(x in output for x in ["25500.25", "25500,25"])
    assert any(x in output for x in ["1550.38", "1550,38"])
    assert any(x in output for x in ["18000.00", "18000"])
