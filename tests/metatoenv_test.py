# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Scipp contributors (https://github.com/scipp)

from metatoenv import main
import yaml


def test_simple_meta_example():
    meta_contents = """
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
    metafile = 'meta.yaml'
    envfile = 'env.yml'

    with open(metafile, "w") as f:
        f.write(meta_contents)

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
