def custom(text: str) -> list[str]:
    return [row.upper() for row in text.split('\n') if len(row) > 0 and row[0] != '#']