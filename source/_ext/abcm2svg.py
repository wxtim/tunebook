"""Convert abc files in ``source/_abcfiles`` making these available for
use in a sphinx doc.
"""

from docutils import nodes
from pathlib import Path
from shlex import split
from subprocess import run

import re
import shutil

from docutils.parsers.rst import Directive


class DepencyMissingError(Exception):
    ...


class abcm2psSubProcFailed(Exception):
    ...


def check_deps():
    """Check that abcm2ps is installed"""
    abcm2ps = run(split('abcm2ps -V'), capture_output=True)
    if abcm2ps.returncode != 0:
        raise DepencyMissingError('You need to have abcm2ps installed')


def clean_abcdir(abcdir):
    """Check file structure for use by the plugin.
    """
    for file_ in abcdir.rglob('*.svg'):
        file_.unlink()
    for file_ in abcdir.rglob('*.rst'):
        file_.unlink()
    for file_ in abcdir.rglob('_*'):
        file_.unlink()


def convert_abcfile(filename):
    """Find Convert ABC to svg for later use.
    """
    svgfile = filename.with_suffix('.svg')
    if svgfile.is_file():
        shutil.rmtree(svgfile)

    # Delete the title field from the files
    text = filename.read_text().splitlines()
    text = [line for line in text if not re.match('^T:', line)]
    fname2 = filename.with_name(f'_{filename.name}')
    fname2.write_text('\n'.join(text))

    # Run abcm2s as a subprocess:
    output = run(
        [
            'abcm2ps',
            '-g',   # Produce SVG output.
            f'{str(fname2)}',
            '-O',   # Output file.
            f'{svgfile}'
        ],
        capture_output=True
    )
    outfile = re.findall('written on (.*) \(', output.stdout.decode())[0]
    Path(outfile).rename(svgfile)
    if output.returncode != 0:
        msg = (
            'ABCM2PS Failed because:\n'
            f'stdout\n------\n{output.stdout}\n\n'
            f'stderr\n------\n{output.stderr}\n'
        )
        raise abcm2psSubProcFailed(msg)


def write_index(categories):
    for category in categories:
        (Path().cwd() / f'source/{category}')


def abc_wrangler(app):
    abcdir = Path().cwd() / 'source/_abcfiles'
    check_deps()
    clean_abcdir(abcdir)
    for abcfile in abcdir.rglob('*.abc'):
        convert_abcfile(abcfile)


def setup(app):
    app.connect('builder-inited', abc_wrangler)
