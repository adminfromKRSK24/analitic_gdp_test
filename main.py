import argparse
import csv
from abc import ABC, abstractmethod
from typing import Any
from tabulate import tabulate
from error import InvalidFileError, InvalidReportError, InvalidFileErrorZero, InvalidCountNameReportError


class BaseFile(ABC):
    def __init__(self):
        self.data: dict[str, Any] = {}

class FileAverageGDP(BaseFile):
    def __init__(self):
        super().__init__()
        self.data["country"] : str = ""
        self.data["gdp"] : float = 0

class Parser():
    def __init__(self):
        self._all_files, self._name_report = Parser.parser_terminal()

    def get_files(self):
        return self._all_files

    def get_name(self):
        return self._name_report[0]

    def check_name(self):
        return self._name_report

    @staticmethod
    def parser_terminal():

        parser = argparse.ArgumentParser()

        parser.add_argument('--files', dest='files', nargs='*', default=[])
        parser.add_argument('--report', dest='name_report', nargs='*', default=[])

        args = parser.parse_args()

        return args.files, args.name_report

class Report(ABC):
    def __init__(self, files, name_report):
        self._all_files : list[str] = files
        self._name_report: str = name_report
        self._all_data_from_files : list[BaseFile] = []
        self._result_report: list[BaseFile] = []

    @abstractmethod
    async def parser_csv(self):
        pass

    @abstractmethod
    def calc(self):
        pass

    @abstractmethod
    def print_report(self):
        pass

class ReportAverageGDP(Report):
    def __init__(self, files, name_report):
        super().__init__(files, name_report)
        self.headers : list[str] = ['№', 'Страна', 'ВВП']

    def parser_csv(self):
        for file in self._all_files:
            try:
                with open(file, 'r') as f:
                    content = csv.DictReader(f)

                    for row in content:
                        cur_file = FileAverageGDP()

                        cur_file.data["country"] = row["country"]
                        cur_file.data["gdp"] = row["gdp"]

                        self._all_data_from_files.append(cur_file)
            except FileNotFoundError:
                print(f"Файл {file} не найден")
                exit(1)

    def calc(self):
        """ Делает расчет ВВП, через множество получаем уникальные страны
            Проходим по всему списку из экземляров файла
            находим совпадения, считаем количество
        """
        cur_set_country : set[str] = set(map(lambda file: file.data["country"], self._all_data_from_files))

        for cur_country in cur_set_country:
            tmp_count = 0
            tmp_value = 0
            tmp_file = FileAverageGDP()

            for cur_file in sorted(self._all_data_from_files, key=lambda c: c.data["country"]):
                if cur_country == cur_file.data["country"]:
                    tmp_count = tmp_count + 1
                    tmp_value = tmp_value + float(cur_file.data["gdp"])

            tmp_file.data["country"] = cur_country
            tmp_file.data["gdp"] = tmp_value / tmp_count

            self._result_report.append(tmp_file)

    def print_report(self):
        table = [
            [i+1, report.data["country"], report.data["gdp"]]
            for i, report in enumerate(sorted(self._result_report, key=lambda c: c.data["gdp"], reverse=True), 0)
        ]

        print(f"{self._name_report}")
        print(tabulate(table, headers=self.headers, tablefmt='grid', floatfmt=".2f"))

REPORT_CLASSES: dict[str, type[Report]] = {
    "average-gdp": ReportAverageGDP,
}

class Conroller():
    def __init__(self):
        self._parser_terminal: Parser = Parser()


    def select_report(self):
        try:
            report = REPORT_CLASSES.get(self._parser_terminal.get_name())

            if report is None:
                raise InvalidReportError()

            if not self._parser_terminal.get_files():
                raise InvalidFileErrorZero()

            if len(self._parser_terminal.check_name()) > 1:
                raise InvalidCountNameReportError()

            if not self._parser_terminal.get_name():
                raise IndexError()

            for file in self._parser_terminal.get_files():
                if str(file[-4:]) != '.csv':
                    raise InvalidFileError()

            cur_report = report(self._parser_terminal.get_files(), self._parser_terminal.get_name())
            cur_report.parser_csv()
            cur_report.calc()
            cur_report.print_report()

        except InvalidFileErrorZero:
            print("Нужно указать хотя бы 1 файл в формате CSV")

        except IndexError:
            print("Не указан отчёт")

        except InvalidCountNameReportError:
            print("Много аргументов для названия отчета")

        except InvalidFileError:
            print("Расширение файла не CSV")
        except InvalidReportError:
            print("Ошибка при выборе отчёта, выбери из существующих:")

            for k in REPORT_CLASSES.keys():
                print(f" - {k}\n")
        except Exception:
            print("Ошибка")



if __name__ == "__main__":

    start = Conroller()
    start.select_report()
