from abc import ABC, abstractmethod
import json
import yaml
from typing import Any
import xml.etree.ElementTree as et


class BaseSerializer(ABC):
    @abstractmethod
    def start_object(self, object_name, object_id) -> None:
        ...

    @abstractmethod
    def add_property(self, name, value) -> None:
        ...

    @abstractmethod
    def to_str(self) -> str:
        ...


class JsonSerializer(BaseSerializer):
    def __init__(self):
        self._current_object = {}

    def start_object(self, object_name, object_id) -> None:
        self._current_object = {
            "id": object_id,
            "name": object_name,
        }

    def add_property(self, name, value) -> None:
        self._current_object[name] = value

    def to_str(self) -> str:
        return json.dumps(self._current_object)


class XmlSerializer(BaseSerializer):
    def __init__(self):
        self._element: Any = None

    def start_object(self, object_name, object_id) -> None:
        self._element = et.Element(object_name, attrib={"id": object_id})

    def add_property(self, name, value) -> None:
        prop = et.SubElement(self._element, name)
        prop.text = value

    def to_str(self) -> str:
        return et.tostring(self._element, encoding="unicode")


class SerializerFactory:
    def __init__(self):
        self._creators = {}

    def register_format(self, format: str, creator: type[BaseSerializer]):
        self._creators[format] = creator

    def get_serializer(self, format: str):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()


class YamlSerializer(JsonSerializer):
    def to_str(self):
        return yaml.dump(self._current_object)


factory = SerializerFactory()
factory.register_format("JSON", JsonSerializer)
factory.register_format("XML", XmlSerializer)
factory.register_format("YAML", YamlSerializer)


class SongSerializer:
    def serialize(self, serializable, format: str) -> str:
        serializer = factory.get_serializer(format)
        serializable.serialize(serializer)
        return serializer.to_str()
