#
# This file is part of Land Cover Classification System Web Service.
# Copyright (C) 2019-2020 INPE.
#
# Land Cover Classification System Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for LCCS-WS."""
from .class_system import ClassificationSystem
from .mappings import MappingGroup
from .utils import Utils


class LCCS:
    """This class implements a Python API client wrapper for LCCS-WS.

    See https://github.com/brazil-data-cube/lccs-ws for more
    information on LCCS-WS.

    :param url: The LCCS-WS server URL.
    :type url: str
    """

    def __init__(self, url, validate=False):
        """Create a LCCS-WS client attached to the given host address (an URL)."""
        self._url = url if url[-1] != '/' else url[0:-1]
        self._classification_systems = {}
        self._validate = validate

    @property
    def get_classification_systems(self):
        """Return the Classification Systems avaliable in service."""
        if len(self._classification_systems) > 0:
            return self._classification_systems.keys()

        url = f'{self._url}/classification_systems'

        data = Utils._get(url)

        for i in data['classification_systems']:
            self._classification_systems[i['name']] = ClassificationSystem(i, self._validate)

        return self._classification_systems.keys()

    @property
    def classification_systems(self):
        """Retrieve the list of names of all available classification systems in the service.

        :returns: List of Classification Systems.
        :rtype: dict
        """
        if self.get_classification_systems:
            pass
        return list(self._classification_systems.keys())

    def classification_system(self, system_id):
        """Return information about the given classification system.

        :param system_id: A str for a given classification_systems_id.
        :type system_id: str

        :returns: A ClassificationSystem.
        :rtype: dict
        """
        if system_id in self._classification_systems.keys() and self._classification_systems[system_id] is not None:
            return self._classification_systems[system_id]
        try:
            data = Utils._get(f'{self._url}/classification_system/{system_id}')
            self._classification_systems[system_id] = ClassificationSystem(data, self._validate)
        except Exception:
            raise KeyError('Could not retrieve information for classification_system: {}'.format(system_id))
        return self._classification_systems[system_id]

    def mappings(self, system_id_source, system_id_target):
        """Return the given classification_system.

        :param system_id_source: A str for a given system_id_source.
        :type system_id_source: str
        :param system_id_target: A str for a given system_id_source.
        :type system_id_target: str

        :returns: Mappings of classification Systems.
        :rtype: list
        """
        try:
            data = Utils._get(f'{self._url}/mappings/{system_id_source}/{system_id_target}')
        except Exception:
            raise KeyError('Could not retrieve mappings for {} and {}'.format(system_id_source, system_id_target))

        data['source_classification_system'] = system_id_source

        data['target_classification_system'] = system_id_target

        return MappingGroup(data, self._validate)

    def available_mappings(self, system_id_source):
        """Return the available mappings of classification system.

        :param system_id_source: A str for a given system_id_source.
        :type system_id_source: str

        :returns: Avaliable Classification Systems Mappings.
        :rtype: list
        """
        result = list()

        try:
            data = Utils._get(f'{self._url}/mappings/{system_id_source}')
        except Exception:
            raise KeyError('Could not retrieve any avaliable mapping for {}'.format(system_id_source))

        [result.append(i['title']) for i in data['links'] if i['rel'] == 'child']

        return result

    def styles(self, system_id):
        """Fetch styles of the a giving classification system.

        :param system_id: A classification System system_id (name).
        :type system_id: str

        :returns: Avaliable Classification Systems Styles.
        :rtype: list
        """
        result = list()
        try:
            data = Utils._get(f'{self._url}/classification_system/{system_id}/styles')
        except Exception:
            raise KeyError('Could not retrieve any style for {}'.format(system_id))

        [result.append(i['title']) for i in data['links'] if i['rel'] == 'child']

        return result

    def get_styles(self, system_id, format_id, path=None):
        """Fetch styles of the a giving classification system.

        :param system_id: A classification system identification (name).
        :type system_id: str

        :param format_id: A classification system format identification (name).
        :type format_id: str

        :param path: Directory path to save fale
        :type format_id: str

        :returns: Style File
        :rtype: File
        """
        try:
            file_name, data = Utils._get(f'{self._url}/classification_system/{system_id}/styles/{format_id}')
        except Exception:
            raise KeyError(f'Could not retrieve any style for {system_id}')

        if path is not None:
            full_path = path + file_name
            return open(full_path, 'wb').write(data)
        return open(file_name, 'wb').write(data)

    def add_classification_system(self, name: str, authority_name: str, description: str,
                                  version: float, file_path: str):
        """Add a new classification system."""
        url = f'{self._url}/classification_systems'

        try:
            file = {'classes': ('classes.json', open(file_path, 'rb'), 'application/json')}
        except RuntimeError:
            raise ValueError(f'Could not open classes file {file_path}. It is a json file ?')

        data = dict()
        data["name"] = name
        data["authority_name"] = authority_name
        data["description"] = description
        data["version"] = version

        try:
            retval = Utils._post(url, data=data, files=file)
        except RuntimeError:
            raise ValueError(f'Could not insert classification system {name}!')

        return ClassificationSystem(retval, self._validate)

    def add_style(self, system_id: str, style_format: str, style_path: str, extension: str):
        """Add a new style format system."""
        url = f'{self._url}/classification_system/{system_id}/styles'

        try:
            style = {'style': (f'style_{system_id}_{style_format}.{extension}', open(style_path, 'rb'),
                               'application/octet-stream')}
        except RuntimeError:
            raise ValueError(f'Could not open style file {style_path}.')

        data = dict()
        data["style_format"] = style_format

        try:
            retval = Utils._post(url, data=data, files=style)
        except RuntimeError:
            raise ValueError('Could not insert style!')

        return retval['message']

    def add_mapping(self, system_id_source: str, system_id_target: str, mappings_path: str):
        """Add new classification system mapping."""
        url = f'{self._url}/mappings/{system_id_source}/{system_id_target}'

        try:
            mapping = {'mappings': ('mappings.json', open(mappings_path, 'rb'), 'application/json')}
        except RuntimeError:
            raise ValueError(f'Could not open mapping file {mappings_path}. It is a json file ?')

        try:
            retval = Utils._post(url, files=mapping)
        except RuntimeError:
            raise ValueError('Could not insert mappings!')

        retval['source_classification_system'] = system_id_source

        retval['target_classification_system'] = system_id_target

        return MappingGroup(retval, self._validate)

    @property
    def url(self):
        """Return the LCSS server instance URL."""
        return self._url

    def __repr__(self):
        """Return the string representation of a lccs object."""
        text = f'lccs("{self.url}")'
        return text

    def __str__(self):
        """Return the string representation of a lccs object."""
        return f'<LCCS [{self.url}]>'

    def _repr_html_(self):
        """HTML repr."""
        classification_systems = str()
        for classification_sys in self.classification_systems:
            classification_systems += f"<li>{classification_sys}</li>"
        return f"""<p>LCCS-WS</p>
                    <ul>
                     <li><b>URL:</b> {self._url}</li>
                     <li><b>Classification Systems:</b></li>
                     <ul>
                     {classification_systems}
                     </ul>
                   </ul>
               """
