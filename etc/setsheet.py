#!/home/tim/miniconda3/envs/utility/bin/python
"""Given a number of tune names
generate a nice set html File.
"""

import sys
from pathlib import Path

TEMPLATE = """
<!doctype html>

<head>
  <meta charset="utf-8">

  <title>{titles}</title>
  <meta name="Created By Tim Pillinger's set creation script.">

  <meta property="og:title" content="{titles}">

  <style>
    html {{
      font-family: "sans-serif";
    }}
  </style>
</head>

<body>
  {tunesections}
</body>
</html>
"""

TUNESECTION = """
  <div id="tunecontainer">
    <h2>{title}</h2>
    <img src="{url}"></img>
  </div>
"""


def main():
    tunes = sys.argv[1:]
    tunesections = []
    tunenames = []
    for tune in tunes:
        tunepath = Path(tune)
        if not Path(tune).is_file():
            raise FileNotFoundError(f'Tune file {tune} cannot be found.')
        tunesections.append(TUNESECTION.format(
            title=tunepath.stem[1:],
            url=str(tunepath)
        ))
        tunenames.append(tunepath.stem[1:])

    tunesections = ''.join(tunesections)

    template = TEMPLATE.format(
        tunesections=tunesections,
        titles='; '.join(tunenames)
    )

    with open(f'{".".join(tunenames)}.html', 'w') as fh:
        fh.write(template)

if __name__ == '__main__':
    main()
