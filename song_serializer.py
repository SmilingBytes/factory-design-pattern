import json
from typing import Any
import xml.etree.ElementTree as et


class JsonSerializer:
    def __init__(self):
        self._current_object = {}

    def start_object(self, object_name, object_id):
        self._current_object = {
            "id": object_id,
            "name": object_name,
        }

    def add_property(self, name, value):
        self._current_object[name] = value

    def to_str(self):
        return json.dumps(self._current_object)


class XmlSerializer:
    def __init__(self):
        self._element: Any = None

    def start_object(self, object_name, object_id):
        self._element = et.Element(object_name, attrib={"id": object_id})

    def add_property(self, name, value):
        prop = et.SubElement(self._element, name)
        prop.text = value

    def to_str(self):
        return et.tostring(self._element, encoding="unicode")


class SerializerFactory:
    def get_serializer(self, format):
        if format == "JSON":
            return JsonSerializer()
        elif format == "XML":
            return XmlSerializer()
        else:
            raise ValueError(format)


factory = SerializerFactory()


class ObjectSerializer:
    def serialize(self, serializable, format):
        serializer = factory.get_serializer(format)
        serializable.serialize(serializer)
        return serializer.to_str()
