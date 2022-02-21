# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Scipp contributors (https://github.com/scipp)

from metatoenv import main
import yaml


def _make_meta_contents(pip_section=False):
    out = """
package:
  name: testpackage
  version: 1.0

source:
  path: ..

requirements:
  build:
    - cmake
    - conan
    - scipp 0.12.*
  run:
    - h5py
    - scipp 0.12.*
    - scipy
"""
    if pip_section:
        out += """
    - pip
    - pip:
      - numpy
      - numba
"""
    out += """

test:
  imports:
    - testpackage
  requires:
    - cmake
    - conan
    - ipympl
    - ipywidgets
  files:
    - cmake-package-test/
  source_files:
    - tests/
  commands:
    - python -m pytest -v tests
    - python cmake-package-test/build.py

build:
  number: 1.0
  script:
    - cmake --preset package


about:
  home: https://github.com/scipp/scipp
  license: BSD-3-Clause
"""
    return out


def test_simple_meta_example():
    metafile = 'meta.yaml'
    envfile = 'env.yml'

    with open(metafile, "w") as f:
        f.write(_make_meta_contents())

    main(metafile=metafile,
         envfile=envfile,
         envname='',
         channels='',
         platform=None,
         extra='',
         mergewith=None,
         pyversion=None)

    with open(envfile, 'r') as f:
        env_contents = yaml.load(f, Loader=yaml.FullLoader)

    expected = {
        'name':
        'env',
        'channels':
        None,
        'dependencies':
        ['cmake', 'conan', 'scipp 0.12.*', 'h5py', 'scipy', 'ipympl', 'ipywidgets']
    }

    assert env_contents == expected


def test_with_pip_section():
    metafile = 'meta.yaml'
    envfile = 'env.yml'

    with open(metafile, "w") as f:
        f.write(_make_meta_contents(pip_section=True))

    main(metafile=metafile,
         envfile=envfile,
         envname='',
         channels='',
         platform=None,
         extra='',
         mergewith=None,
         pyversion=None)

    with open(envfile, 'r') as f:
        env_contents = yaml.load(f, Loader=yaml.FullLoader)

    expected = {
        'name':
        'env',
        'channels':
        None,
        'dependencies': [
            'cmake', 'conan', 'scipp 0.12.*', 'h5py', 'scipy', 'pip', {
                'pip': ['numpy', 'numba']
            }, 'ipympl', 'ipywidgets'
        ]
    }

    assert env_contents == expected


def test_with_channels():
    metafile = 'meta.yaml'
    envfile = 'env.yml'

    with open(metafile, "w") as f:
        f.write(_make_meta_contents())

    main(metafile=metafile,
         envfile=envfile,
         envname='',
         channels=['channel_one', 'channel_two'],
         platform=None,
         extra='',
         mergewith=None,
         pyversion=None)

    with open(envfile, 'r') as f:
        env_contents = yaml.load(f, Loader=yaml.FullLoader)

        expected = {
            'name':
            'env',
            'channels': ['channel_one', 'channel_two'],
            'dependencies':
            ['cmake', 'conan', 'scipp 0.12.*', 'h5py', 'scipy', 'ipympl', 'ipywidgets']
        }

    assert env_contents == expected


def test_simple_meta_example():
    metafile = 'meta.yaml'
    envfile = 'env.yml'

    with open(metafile, "w") as f:
        f.write(_make_meta_contents())

    main(metafile=metafile,
         envfile=envfile,
         envname='',
         channels='',
         platform=None,
         extra='',
         mergewith=None,
         pyversion=None)

    with open(envfile, 'r') as f:
        env_contents = yaml.load(f, Loader=yaml.FullLoader)

    expected = {
        'name':
        'env',
        'channels':
        None,
        'dependencies':
        ['cmake', 'conan', 'scipp 0.12.*', 'h5py', 'scipy', 'ipympl', 'ipywidgets']
    }

    assert env_contents == expected
