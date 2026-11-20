def median(values):
    """Медиана: середина отсортированного списка."""
    values = sorted(values)
    if len(values) % 2 == 0:
        return  (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2
    else:
        return values[len(values) // 2]

