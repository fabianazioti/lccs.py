#
# This file is part of Python Client Library for the LCCS-WS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Python Client Library for the LCCS Web Service."""
import re
import httpx
import jinja2
from jsonschema import RefResolver, validate
from pkg_resources import resource_filename

# Caminho dos schemas e templates
base_schemas_path = resource_filename(__name__, 'jsonschemas/')
templateLoader = jinja2.FileSystemLoader(searchpath=resource_filename(__name__, 'templates/'))
templateEnv = jinja2.Environment(loader=templateLoader)

class Utils:
    """Utils class for handling HTTP requests and other utility functions."""

    @staticmethod
    def _get(url, access_token=None, params=None):
        """Query the LCCS-WS using HTTP GET verb and return the result as a JSON document.

        Args:
            url (str): The URL to query, must be a valid LCCS-WS endpoint.
            params (dict, optional): Dictionary, list of tuples, or bytes to send in the query string.

        Returns:
            dict: The parsed JSON response from the server.

        Raises:
            ValueError: If the response is not a valid JSON or cannot be processed.
        """
<<<<<<< HEAD
        try:
            # Realiza a requisição GET usando httpx
            response = httpx.get(url, params=params)
            response.raise_for_status()  # Garante que a resposta foi bem-sucedida
=======
        _headers = {}
        if access_token != None:
            _headers = {
                "x-api-key": access_token
            }

        response = requests.get(url, params=params, headers=_headers)
>>>>>>> 7a0ee79d16a5ad588473daacf7744f600b812f30

            # Verifica o tipo de conteúdo da resposta
            content_type = response.headers.get('content-type', '').lower()

            if 'application/octet-stream' in content_type:
                content = response.headers.get('content-disposition')
                file_name = re.findall('filename=(.+)', content)[0] if content else 'unknown_file'
                return file_name, response.content

            if content_type not in ('application/json', 'application/geo+json'):
                raise ValueError(f'HTTP response is not JSON: Content-Type: {content_type}')

            return response.json()

        except httpx.RequestError as e:
            raise ValueError(f"An error occurred while requesting {url}: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Invalid JSON response from {url}: {str(e)}")

    @staticmethod
<<<<<<< HEAD
    def _post(url, data=None, json=None, files=None):
        """Send a POST request to the specified URL.
=======
    def _post(url, access_token, data=None, json=None, files=None):
        """Request post method."""
        _headers = {}
        if access_token != None:
            _headers = {
                "x-api-key": access_token
            }

        response = requests.post(url, headers=_headers, data=data, files=files, json=json)
>>>>>>> 7a0ee79d16a5ad588473daacf7744f600b812f30

        Args:
            url (str): The URL to send the POST request.
            data (dict, optional): The form data to include in the request.
            json (dict, optional): The JSON body to send in the request.
            files (dict, optional): Files to be uploaded.

        Returns:
            dict: The parsed JSON response from the server.

        Raises:
            ValueError: If the request fails or the response cannot be parsed.
        """
        try:
            response = httpx.post(url, data=data, files=files, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise ValueError(f"An error occurred while sending POST request to {url}: {str(e)}")

    @staticmethod
<<<<<<< HEAD
    def _delete(url, params=None):
        """Send a DELETE request to the specified URL.
=======
    def _delete(url, access_token, params=None):
        """Request delete method."""
        _headers = {}
        if access_token != None:
            _headers = {
                "x-api-key": access_token
            }

        response = requests.delete(url, params=params, headers=_headers)
>>>>>>> 7a0ee79d16a5ad588473daacf7744f600b812f30

        Args:
            url (str): The URL to send the DELETE request.
            params (dict, optional): The parameters to include in the DELETE request.

        Returns:
            httpx.Response: The raw HTTP response from the server.

        Raises:
            ValueError: If the request fails.
        """
        try:
            response = httpx.delete(url, params=params)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            raise ValueError(f"An error occurred while sending DELETE request to {url}: {str(e)}")

    @staticmethod
    def validate(lccs_object):
        """Validate a LUCC object using its JSON schema.

        Args:
            lccs_object (object): The LUCC object to be validated.

        Raises:
            ValidationError: If the object fails to validate.
        """
        resolver = RefResolver(f"file://{base_schemas_path}/{lccs_object}")
        validate(lccs_object, lccs_object._schema, resolver=resolver)

    @staticmethod
    def render_html(template_name, **kwargs):
        """Render a Jinja2 HTML template.

        Args:
            template_name (str): The name of the template to render.
            **kwargs: The context variables to pass to the template.

        Returns:
            str: The rendered HTML template.
        """
        template = templateEnv.get_template(template_name)
        return template.render(**kwargs)

    @staticmethod
    def get_id_by_name(name, classes):
        """Get the ID of a class by its name.

        Args:
            name (str): The name of the class.
            classes (list): A list of class objects containing 'name' and 'id' attributes.

        Returns:
            str: The ID of the class with the matching name.

        Raises:
            IndexError: If no matching class is found.
        """
        try:
            return next(class_obj for class_obj in classes if class_obj['name'] == name)['id']
        except StopIteration:
            raise ValueError(f"Class with name '{name}' not found")
