# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import json
import jsonschema
from pkg_resources import resource_stream

from .serializer import get_serializer

class SerializedMessage(object):
    def __init__(self, content_type: str, payload: bytes) -> None:
        """
        Creates a new container for a serialized IDMEFv2 message.

        @param content_type:
            The MIME type associated with the serialized payload.

            To promote interoperability, this SHOULD be a content type
            registered in IANA. A private MIME content type MAY be used
            when it is known that the next processing entity has support
            for that type.

            Whenever a private MIME content type is used, it MUST
            follow the naming conventions set forth by IANA.

        @param payload:
            The IDMEFv2 message, as a serialized payload.
        """
        self.content_type = content_type
        self.payload = payload

    def get_content_type(self) -> str:
        """
        Returns the content type associated with the serialized payload.
        """
        return self.content_type

    def __bytes__(self) -> bytes:
        """
        The serialized payload.
        """
        return self.payload


class Message(dict):
    _VERSIONS = {
        None: 'IDMEFv2_0.1.schema',
        '0.1': 'IDMEFv2_0.1.schema',
    }

    def __init__(self):
        # The messages are empty right after initialization.
        pass

    def validate(self) -> None:
        schema_file = self._VERSIONS.get(self.get('Version'), self._VERSIONS[None])
        stream = resource_stream('idmef.schemas', schema_file)
        try:
            jsonschema.validate(self, json.load(stream))
        finally:
            stream.close()

    def serialize(self, content_type: str) -> SerializedMessage:
        serializer = get_serializer(content_type)
        self.validate()
        payload = serializer.serialize(self)
        return SerializedMessage(content_type, payload)

    @classmethod
    def unserialize(self, payload: SerializedMessage) -> 'Message':
        serializer = get_serializer(payload.get_content_type())
        fields = serializer.unserialize(bytes(payload))
        message = self()
        message.update(fields)
        message.validate()
        return message
