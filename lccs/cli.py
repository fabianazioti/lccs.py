#
# This file is part of Land Cover Classification System Web Service.
# Copyright (C) 2020-2021 INPE.
#
# Land Cover Classification System Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Command line interface for the LCCS-WS client."""
import click

from .lccs import LCCS


class Config:
    """A simple decorator class for command line options."""

    def __init__(self):
        """Initialize of Config decorator."""
        self.url = None
        self.service = None
        self.access_token = None
        self.language = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--url', default='http://127.0.0.1:5000/',
              help='The LCCS server address (an URL).')
@click.option('--access-token', default=None, help='Personal Access Token of the BDC Auth')
@click.version_option()
@pass_config
def cli(config, url, access_token=None, language=None):
    """LCCS-WS Client on command line."""
    config.url = url
    config.service = LCCS(url=url, access_token=access_token, language=language)


@cli.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classification_systems(config: Config, verbose):
    """Return the list of available classification systems in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available classification systems... ',
                    bold=False, fg='black')

    if verbose:
        for cs in config.service.classification_systems:
            click.secho(f'\t\t- {cs}', bold=True, fg='green')
    else:
        for cs in config.service.classification_systems:
            click.secho(f'{cs}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classification_system_description(config: Config, system, verbose):
    """Return information for a given classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the classification system metadata... ',
                    bold=False, fg='black')

    retval = config.service.classification_system(system=system)

    for ds_key, ds_value in retval.items():
        click.secho(f'\t- {ds_key}: {ds_value}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def classes(config: Config, system, verbose):
    """Return the list of available classes given a classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the the list of classes for a given classification system.... ',
                    bold=False, fg='black')

    class_system = config.service.classification_system(system=system)

    if verbose:
        for cv in class_system.classes():
            click.secho(f'\t\t- {cv.name}', bold=True, fg='green')
    else:
        for cv in class_system.classes():
            click.secho(f'{cv.name}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('--system_class', type=click.STRING, required=True, help='The class name or id.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def class_describe(config: Config, system, system_class, verbose):
    """Return information for a classes given a classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the class metadata... ',
                    bold=False, fg='black')

    classification_system = config.service.classification_system(system=system)

    retval = classification_system.classes(system_class)

    for ds_key, ds_value in retval.items():
        click.secho(f'\t- {ds_key}: {ds_value}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def available_mappings(config: Config, system, verbose):
    """Return the list of available mappings."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available for a given classification system ... ',
                    bold=False, fg='black')
    
    retval = config.service.available_mappings(system_source=system)

    if verbose:
        for mp in retval:
            click.secho(f'\t\t- {mp}', bold=True, fg='green')
    else:
        for mp in retval:
            click.secho(f'{mp}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system-source', type=click.STRING, required=True,
              help='The classification system source (Identifier by name-version or the ID).')
@click.option('--system-target', type=click.STRING, required=True, default=None,
              help='The classification system target (Identifier by name-version or the ID).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def mappings(config: Config, system_source, system_target, verbose):
    """Return the mapping."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the mapping ... ',
                    bold=False, fg='black')
    
    retval = config.service.mappings(system_source=system_source, system_target=system_target)

    if verbose:
        click.secho(f'\t- {retval}', bold=True, fg='green')
        click.secho('\tFinished!', bold=False, fg='black')
    else:
        click.secho(f'\t- {retval}', bold=True, fg='green')


@cli.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def style_formats(config: Config, verbose):
    """Return the list of available style formats in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available styles formats... ',
                    bold=False, fg='black')

    if verbose:
        for style in config.service.available_style_formats():
            click.secho(f'\t\t- {style.name}', bold=True, fg='green')
    else:
        for style in config.service.available_style_formats():
            click.secho(f'{style.name}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def styles(config: Config, system_name, verbose):
    """Return the style format available for a specific classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available styles formats... ',
                    bold=False, fg='black')

    if verbose:
        for style in config.service.style_formats(system_source_name=system_name):
            click.secho(f'\t\t- {style.name}', bold=True, fg='green')
    else:
        for style in config.service.style_formats(system_source_name=system_name):
            click.secho(f'{style.name}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('--style_format_name', type=click.STRING, required=True, default=None,
              help='The style format name.')
@click.option('-o', '--output', help='Output to a file', type=click.Path(dir_okay=True), required=False)
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def style_file(config: Config, system_name, style_format_name, output, verbose):
    """Return and save the style for a specific classification system and style format in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tRetrieving the list of available styles formats... ',
                    bold=False, fg='black')

    if output:
        config.service.get_style(system_name=system_name, format_name=style_format_name, path=output)
        click.secho(f'Style file save in {output}', bold=True, fg='green')

    config.service.get_style(system_name=system_name, format_name=style_format_name)

    click.secho(f'Style file save', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name_source', type=click.STRING, required=True,
              help='The classification system source (Identifier by name-version).')
@click.option('--system_name_target', type=click.STRING, required=True, default=None,
              help='The classification system target (Identifier by name-version).')
@click.option('--mappings_path', type=click.Path(exists=True), required=True,  help='Json file with the mapping')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_mapping(config: Config, system_name_source, system_name_target, mappings_path, verbose):
    """Add a mapping between classification systems."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new mapping ... ', bold=False, fg='black')

    config.service.add_mapping(system_name_source=system_name_source,
                               system_name_target=system_name_target,
                               mappings=mappings_path)

    click.secho(f'Added Mapping between {system_name_source} and '
                f'{system_name_target}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('--style_format_name', type=click.STRING, required=True, default=None,
              help='The style format name.')
@click.option('--style_path', type=click.Path(exists=True), required=True,  help='The style file path.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_style(config: Config, system_name, style_format_name, style_path, verbose):
    """Add a classification system style."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system style ... ', bold=False, fg='black')

    config.service.add_style(system_name=system_name,
                             format_name=style_format_name,
                             style_path=style_path)

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--style_format_name', type=click.STRING, required=True, default=None,
              help='The style format name.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_style_format(config: Config, style_format_name, verbose):
    """Add a classification system style."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system style ... ', bold=False, fg='black')

    config.service.add_style_format(name=style_format_name)

    click.secho('Added!', bold=True, fg='black')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='The classification system name.')
@click.option('--authority_name', type=click.STRING, required=True, default=None,
              help='The classification system authority name.')
@click.option('--description', type=click.STRING, required=True, default=None,
              help='The classification system description.')
@click.option('--version', type=click.STRING, required=True, default=None,
              help='The classification system version.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_classification_system(config: Config, name, authority_name, description, version, verbose):
    """Add a new classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new classification system ... ', bold=False, fg='black')

    cs = config.service.add_classification_system(name=name,
                                                  authority_name=authority_name,
                                                  description=description,
                                                  version=version)

    click.secho(f' Classification System {cs["name"]} added!', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('--classes_path', type=click.Path(exists=True), required=True,  help='Json file with classes')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def add_classes(config: Config, system_name, classes_path, verbose):
    """Add a mapping between classification systems."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tAdding new mapping ... ', bold=False, fg='black')

    config.service.add_classes(system_name=system_name, classes=classes_path)

    click.secho(f'Added classes for {system_name}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_classification_systems(config: Config, system_name, verbose):
    """Delete a specific classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the classification system ... ',
                    bold=False, fg='black')

    config.service.delete_classification_system(system_name=system_name)

    click.secho(f'\t - Deleted classification system: {system_name}!', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('--class_name', type=click.STRING, required=True, help='The class name.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_class(config: Config, system_name, class_name, verbose):
    """Delete class of a classification system in the service provider."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting class... ',
                    bold=False, fg='black')

    config.service.delete_class(system_name=system_name, class_name=class_name)

    click.secho(f'\t Deleted class {class_name} of classification system {system_name}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--style_format_name', type=click.STRING, required=True, default=None,
              help='The style format name.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_style_format(config: Config, style_format_name, verbose):
    """Delete a style format."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the style format ... ', bold=False, fg='black')

    config.service.delete_style_format(format_name=style_format_name)

    click.secho(f'\t Deleted style format {style_format_name}', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name', type=click.STRING, required=True,
              help='The classification system (Identifier by name-version).')
@click.option('--style_format_name', type=click.STRING, required=True, default=None,
              help='The style format name.')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_style(config: Config, system_name, style_format_name, verbose):
    """Delete a style for a classification system."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the style ... ', bold=False, fg='black')

    config.service.delete_style(system_name=system_name, format_name=style_format_name)

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


@cli.command()
@click.option('--system_name_source', type=click.STRING, required=True,
              help='The classification system source (Identifier by name-version).')
@click.option('--system_name_target', type=click.STRING, required=True, default=None,
              help='The classification system target (Identifier by name-version).')
@click.option('-v', '--verbose', is_flag=True, default=False)
@pass_config
def delete_mapping(config: Config, system_name_source, system_name_target, verbose):
    """Delete a mapping between classification systems."""
    if verbose:
        click.secho(f'Server: {config.url}', bold=True, fg='black')
        click.secho('\tDeleting the mapping ... ', bold=False, fg='black')

    config.service.delete_mapping(system_name_source=system_name_source, system_name_target=system_name_target)

    click.secho(f'Mapping between {system_name_source} and '
                f'{system_name_target} deleted!', bold=True, fg='green')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')
