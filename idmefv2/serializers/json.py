# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import json

from ..exceptions import SerializationError
from ..message import Message
from ..serializer import Serializer


class JSONSerializer(Serializer):
    def serialize(self, message: Message) -> bytes:
        try:
            payload = json.dumps(message).encode('utf-8')
        except:
            raise SerializationError()
        return payload

    def unserialize(self, payload: bytes) -> dict:
        try:
            message = json.loads(payload)
        except:
            raise SerializationError()
        return message
