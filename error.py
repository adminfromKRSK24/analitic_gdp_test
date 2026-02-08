class InvalidReportError(ValueError):
    """Вызывается, когда указан несуществующий тип отчёта"""
    pass

class InvalidFileError(ValueError):
    """Вызывается, когда файл имеет неподходящее расширение"""
    pass

class InvalidFileErrorZero(ValueError):
    """Вызывается, когда файлы не переданы"""
    pass

class InvalidCountNameReportError(ValueError):
    """Вызывается, когда навазние отчета не передано"""
    pass


