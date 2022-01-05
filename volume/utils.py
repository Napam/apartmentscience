import json
from pygments import highlight, lexers, formatters
import datetime as dt

isoNow = lambda: dt.datetime.now().isoformat()

def jprint(data: dict, file: str | None = None, indent: int = 4) -> str | None:
    dump = json.dumps(data, indent=indent)
    if file:
        with open(file, "w+") as f:
            f.write(dump)
    else:
        print(highlight(dump, lexers.JsonLexer(),
              formatters.TerminalFormatter(bg='dark')))