#
# This file is part of Python Client Library for the LCCS-WS.
# Copyright (C) 2020 INPE.
#
# Python Client Library for the LCCS-WS is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""LCCS Python Client examples."""

from lccs import LCCS

# Change to the LCCS-WS URL you want to use.
service = LCCS("http://brazildatacube.dpi.inpe.br/dev/lccs/")

# Save Style File
service.get_style(system_name='PRODES-1.0', format_name='QGIS')

# Save Style File passing the path directory
service.get_style(system_name='PRODES-1.0', format_name='QGIS', path='/home/user/Downloads/')
