class InvalidReportError(ValueError):
    """Вызывается, когда указан несуществующий тип отчёта"""
    pass

class InvalidFileError(ValueError):
    """Вызывается, когда файл имеет неподходящее расширение"""
    pass

