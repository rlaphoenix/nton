from datetime import datetime


def get_copyright_years() -> str:
    start_year = 2022
    current_year = datetime.now().year
    if start_year == current_year:
        return str(start_year)
    return f"{start_year}-{current_year}"
