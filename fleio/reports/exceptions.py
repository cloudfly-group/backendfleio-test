class ReportException(Exception):
    pass


class InvalidArgument(ReportException):
    pass


class ReportIsAlreadyGenerating(ReportException):
    pass


class RevenueReportTimezoneError(ReportException):
    pass
