import re
from glob import glob
from pathlib import Path
from shlex import split
from subprocess import run

LIBRARY = Path(__file__).parent.parent / 'source/_abcfiles'

x = run(
    split(f'grep -rl "COLLECTION:CAROLS" {LIBRARY}'),
    capture_output=True,
    text=True
    )

destination = LIBRARY / 'CarolBook.abc'
with open(destination, 'w+') as dfh:
    for i, file in enumerate(x.stdout.split('\n')):
        file = Path(file)
        if not file.name.startswith('_'):
            try:
                dfh.write(file.read_text())
                dfh.write('\n\n')
            except:
                pass

