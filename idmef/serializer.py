# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import abc
import pkg_resources
import warnings

from collections.abc import Callable

_serializers = None


class Serializer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serialize(self, message: 'Message') -> bytes:
        """
        Returns the serialized form of an IDMEFv2 message.

        @param message:
            The IDMEFv2 message to serialize.

        This method MUST raise a SerializationException exception when
        the serialization cannot proceed (e.g. due to a lack of resources).
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def unserialize(self, payload: bytes) -> 'Message':
        """
        Unserializes a serialized IDMEFv2 message.

        @param payload:
            An IDMEFv2 message in serialized form.

        This method MUST raise a SerializationException exception when
        the payload cannot be unserialized (e.g. due to data corruption).
        """
        raise NotImplementedError()


def get_serializer(content_type: str) -> 'Serializer':
    """
    This methods returns a serializer/unserializer compatible
    with the requested MIME content type.

    @param content_type:
        MIME type for which a serializer must be returned.

    This method MUST raise a KeyError exception when a serializer
    compatible with the given MIME type cannot be found.
    """
    global _serializers

    if _serializers is None:
        _serializers = {}
        for entry_point in pkg_resources.iter_entry_points('idmef.serializer'):
            try:
                cls = entry_point.load()
                if issubclass(cls, Serializer):
                    _serializers[entry_point.name] = cls
            except Exception as e:
                warnings.warn(str(e), ResourceWarning)

    return _serializers[content_type]()
