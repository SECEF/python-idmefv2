# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import glob
import os
import shutil

from setuptools import setup, find_packages
from distutils.command.build import build as orig_build
from setuptools.command.develop import develop as orig_develop

VERSION = "0.0.0"


def copy_schemas(basedir):
    schemasdir = os.path.join(basedir, 'schemas')
    for f in glob.glob('data/*.schema'):
        shutil.copy2(f, schemasdir)

class build(orig_build):
    def run(self):
        res = orig_build.run(self)
        copy_schemas(os.path.join(self.build_purelib, self.distribution.metadata.get_name()))
        return res

class develop(orig_develop):
    def run(self):
        res = orig_develop.run(self)
        copy_schemas(os.path.join('.', self.distribution.metadata.get_name()))
        return res


setup(
    name="idmefv2",
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
    install_requires=["setuptools", "jsonschema"],
    packages=find_packages("."),
    cmdclass={'build': build, 'develop': develop},
    zip_safe=False,
    entry_points={
        'idmefv2.serializer': [
            'application/json = idmefv2.serializers.json:JSONSerializer',
            'text/json = idmefv2.serializers.json:JSONSerializer',
        ],
    },
)
