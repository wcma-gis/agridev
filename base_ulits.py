import platform
import pandas as pd

def to_readable_date(date):
    date = pd.to_datetime(date)
    fmt = '%-d %B %Y' if platform.system() != "Windows" else '%#d %B %Y'
    return date.strftime(fmt)
