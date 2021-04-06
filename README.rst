IDMEFv2 Modelization library
############################

This repository contains a Python library that provides modelization features
for the Intrusion Detection Message Exchange Format version 2 (IDMEFv2).
It is part of the `SECEF <https://www.secef.net/>` project.

It can be used to represent IDMEFv2 messages in memory, validate them and
serialize/unserialize them for exchange with other systems.

This code is currently in an experimental status and is regularly kept in sync
with the development status of the IDMEFv2 format, as part of the SECEF project.

You can find more information about the previous version (v1) of the
Intrusion Detection Message Exchange Format
in `RFC 4765 <https://tools.ietf.org/html/rfc4765>`.

Visit https://www.secef.net/ for more information about IDMEFv2's status
and development progress.

Installation
============

The following prerequisites must be installed on your system to install
and use this library:

* Python 3.6 or later
* The Python `setuptools <https://pypi.org/project/setuptools/>` package
  (usually available as a system package under the name ``python3-setuptools``)
* The Python `jsonschema <https://pypi.org/project/jsonschema/>` package
  (usually available as a system package under the name ``python3-jsonschema``)

To install the library, simply run:

..  sourcecode:: sh

    # Replace "python3" with the full path to the Python 3 interpreter
    # if necessary.
    sudo python3 install setup.py

Usage
=====

Message modelization
--------------------

A new message can be created by instantiating the ``idmef.Message`` class.
This object can then be used like a regular Python dictionary:

..  sourcecode:: python

    # Import the Message class
    from idmef import Message

    # Import other modules if necessary
    import uuid
    from datetime import datetime

    # Keep track of the current date/time for later reference.
    now = datetime.now().isoformat('T')

    # Create the message and set its various properties.
    msg = Message()
    msg['Version'] = '0.1'
    msg['ID'] = str(uuid.uuid4())
    msg['CreateTime'] = now
    msg['DetectTime'] = now
    msg['CategoryRef'] = 'ENISA'
    msg['Category'] = []
    msg['Description'] = 'Someone tried to login as root from 12.34.56.78 '\
                         'port 1806 using the password method'
    msg['Severity'] = 'medium'
    msg['Ref'] = []
    msg['Agent'] = {
        'Name': 'prelude-lml',
        'ID': str(uuid.uuid4()),
        'Category': ['LOG'],
        'IP4': '127.0.0.1',
        'IP6': '::1',
    }
    msg['Source'] = []
    msg['Target'] = []

    # Do something with the message (e.g. send it to a SIEM)


Message validation
------------------

You can validate an IDMEFv2 message using its ``validate()`` method.
A `validation error <https://python-jsonschema.readthedocs.io/en/stable/errors/>`
is raised if the message is invalid.

E.g.

..  sourcecode:: python

    try:
        msg.validate()
    except jsonschema.exceptions.ValidationError as e:
        print("Validation failure: %s" % (e, ))
    else:
        print("The message is valid")


Message serialization/unserialization
-------------------------------------

Before the message can be sent to a remote system, it must be serialized.

To serialize a message, use the ``serialize()`` method, e.g.

..  sourcecode:: python

    result = msg.serialize('application/json')

The argument given to the ``serialize()`` method specifies the expected
MIME content type for the resulting payload.

For the time being, only the ``application/json`` content type is supported,
which results in a JSON-encoded message.

Likewise, when a message is received from a foreign system, it must be
unserialized before it can be used. This is achieved using the ``unserialize()``
class method.

Please note that the received data must be encapsulated using an instance
of the ``SerializedMessage`` class first so that the proper class can be used
during the unserialization process based on the payload's content type.

E.g.

..  sourcecode:: python

    from idmef import Message, SerializedMessage

    # Instantiate a SerializedMessage based on the received data.
    # The first argument specifies the MIME content type for the data.
    payload = SerializedMessage('application/json', data)

    # Unserialize the message for later use
    msg = Message.unserialize(payload)

    # Do something with the message (e.g. store it in a database)


Contributions
=============

All contributions must be licensed under the BSD 2-clause license.
See the LICENSE file inside this repository for more information.

To improve coordination between the various contributors, we kindly ask
that new contributors subscribe to the `SECEF mailing list
<https://www.freelists.org/list/secef>` as a way to introduce themselves.
