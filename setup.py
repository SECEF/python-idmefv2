# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import glob
import io
import os
import subprocess
import sys

from setuptools import setup, find_packages
from distutils.command.build import build as orig_build
from setuptools.command.develop import develop as orig_develop

VERSION = "0.0.0"


def compile_schemas(basedir):
    schemasdir = os.path.join(basedir, 'schemas')
    for f in glob.glob('data/*.schema.in'):
        fname = os.path.basename(f[:-3])
        with io.open(f, 'rb') as schema:
            subprocess.check_output(["gcc", "-P", "-E", "-", "-o", os.path.join(schemasdir, fname)],
                                    input=schema.read())

class build(orig_build):
    def run(self):
        res = orig_build.run(self)
        compile_schemas(os.path.join(self.build_purelib, self.distribution.metadata.get_name()))
        return res

class develop(orig_develop):
    def run(self):
        res = orig_develop.run(self)
        compile_schemas(os.path.join('.', self.distribution.metadata.get_name()))
        return res


setup(
    name="idmef",
    version=VERSION,
    maintainer="Prelude Team",
    maintainer_email="contact.secef@csgroup.eu",
    license="GPL",
    url="https://www.secef.net",
    description="Modelization and serialization library for IDMEF v2",
    long_description="""
""",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: System :: Monitoring"
    ],
    install_requires=["setuptools"],
    packages=find_packages("."),
    cmdclass={'build': build, 'develop': develop},
    zip_safe=False,
    entry_points={
        'idmef.serializer': [
            'application/json = idmef.serializers.json:JSONSerializer',
            'text/json = idmef.serializers.json:JSONSerializer',
        ],
    },
)
