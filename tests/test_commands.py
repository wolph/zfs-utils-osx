"""Exercise command construction without touching disks or invoking ZFS."""

import argparse
import os
import subprocess
import sys

import pytest

from zfs_utils_osx import argparse_utils, constants, load, main, metadata, utils


@pytest.mark.parametrize('value,minimum', [('2', 1), ('0', -1)])
def test_greater_than_accepts(value, minimum):
    # type: (str, int) -> None
    assert argparse_utils.greater_than(value, int, minimum) == int(value)


@pytest.mark.parametrize('value', ['1', '0', '-1'])
def test_greater_than_rejects_boundary(value):
    # type: (str) -> None
    with pytest.raises(argparse.ArgumentTypeError, match='greater than'):
        argparse_utils.greater_than(value, int, 1)


@pytest.mark.parametrize('mode,expected', [
    ('raidz', 4), ('raidz1', 4), ('raidz2', 3), ('raidz3', 2), ('mirror', 1),
])
def test_pool_capacity(mode, expected):
    # type: (str, int) -> None
    assert constants.ZPOOL_TYPES[mode](5) == expected


@pytest.mark.parametrize('values,expected', [
    ((None, None, 'last'), 'last'), ((0, 3), 0), ((False, True), False),
    (('', 'other'), ''), ((None, None), None),
])
def test_coalesce(values, expected):
    # type: (tuple, object) -> None
    assert utils.coalesce(*values) == expected


def test_execute_formats_command(monkeypatch, capsys):
    # type: (object, object) -> None
    calls = []  # type: list

    def output(command, shell):
        # type: (str, bool) -> str
        calls.append((command, shell))
        return 'result'

    monkeypatch.setattr(subprocess, 'check_output', output)
    context = {'name': 'spam', 'no_op': False}  # type: dict
    assert utils.execute(context, '\n tool  %(name)s\n %(extra_args)s', '-a', '-b') == 'result'
    assert calls == [('tool spam -a -b', True)]
    assert capsys.readouterr().out == '# tool spam -a -b\n'


def test_execute_dry_run(capsys):
    # type: (object) -> None
    assert utils.execute({'no_op': True}, 'tool') is None
    assert capsys.readouterr().out == '# tool\n'


def test_execute_propagates_error(monkeypatch):
    # type: (object) -> None
    def output(command, shell):
        # type: (str, bool) -> None
        raise subprocess.CalledProcessError(2, command)

    monkeypatch.setattr(subprocess, 'check_output', output)
    with pytest.raises(subprocess.CalledProcessError) as error:
        utils.execute({'no_op': False}, 'tool')
    assert error.value.returncode == 2


def test_parser_defaults_and_metadata():
    # type: () -> None
    args = main.get_parser().parse_args(['zpool', 'spam'])  # type: argparse.Namespace
    assert (args.count, args.size, args.type) == (3, 10, 'raidz')
    assert args.prefix == '%(pool_name)s_'
    assert metadata.__package_name__ == 'zfs-utils-osx'
    assert metadata.__version__ == '1.1.0'


@pytest.mark.parametrize('option,value', [('--count', '1'), ('--size', '0')])
def test_parser_rejects_invalid_sizes(option, value):
    # type: (str, str) -> None
    with pytest.raises(SystemExit) as error:
        main.get_parser().parse_args(['zpool', option, value, 'spam'])
    assert error.value.code == 2


@pytest.mark.parametrize('overwrite', [False, True])
def test_create_pool_commands(monkeypatch, overwrite):
    # type: (object, bool) -> None
    calls = []  # type: list

    def output(command, shell):
        # type: (str, bool) -> str
        assert shell is True
        calls.append(command)
        if command.startswith('hdiutil attach'):
            return '/dev/disk%d\n' % len(calls)
        return ''

    monkeypatch.setattr(subprocess, 'check_output', output)
    argv = ['zfs.py', 'zpool', '-c', '2', '-s', '2.5', '-t', 'mirror',
            '-m', '/mnt/%(pool_name)s', '--postfix', '_image', 'spam']  # type: list
    if overwrite:
        argv.append('-o')
    monkeypatch.setattr(sys, 'argv', argv)
    main.main()
    extra = '-ov' if overwrite else ''  # type: str
    assert calls == [
        'hdiutil create -size 2.5g -volname spam_00_image -type SPARSE -layout NONE %s spam_00_image' % extra,
        'hdiutil attach -nomount  spam_00_image.sparseimage',
        'hdiutil create -size 2.5g -volname spam_01_image -type SPARSE -layout NONE %s spam_01_image' % extra,
        'hdiutil attach -nomount  spam_01_image.sparseimage',
        'sudo zpool create  -f -m /mnt/spam spam mirror /dev/disk2 /dev/disk4',
    ]


def test_create_dry_run_preserves_integer_division(capsys):
    # type: (object) -> None
    args = main.get_parser().parse_args(['zpool', '-n', '-c', '4', 'spam'])  # type: argparse.Namespace
    args.func(args)
    assert args.image_size == 3
    assert args.effective_size == 9
    output = capsys.readouterr().out  # type: str
    assert output.count('# hdiutil create') == 4
    assert output.count('# hdiutil attach') == 4
    assert 'sudo zpool create' not in output


@pytest.mark.parametrize('failure,message,exit_code', [
    ('hdiutil create', 'Unable to create a new image', 1),
    ('hdiutil attach', 'Unable to attach image', 1),
    ('sudo zpool create', '', None),
])
def test_create_failures(monkeypatch, capsys, failure, message, exit_code):
    # type: (object, object, str, str, object) -> None
    calls = []  # type: list

    def output(command, shell):
        # type: (str, bool) -> str
        calls.append(command)
        if command.startswith(failure):
            raise subprocess.CalledProcessError(2, command)
        return '/dev/disk1\n'

    monkeypatch.setattr(subprocess, 'check_output', output)
    args = main.get_parser().parse_args(['zpool', '-c', '2', 'spam'])  # type: argparse.Namespace
    exception = SystemExit if exit_code else subprocess.CalledProcessError  # type: type
    with pytest.raises(exception) as error:
        args.func(args)
    if exit_code:
        assert error.value.code == exit_code
        assert message in capsys.readouterr().out
    else:
        assert error.value.returncode == 2
    assert calls[-1].startswith(failure)


def fake_walk(monkeypatch, files):
    # type: (object, list) -> None
    def walk(path):
        # type: (str) -> list
        assert path == os.path.abspath(os.path.expanduser('~/zfs/'))
        return [('/images', [], files), ('/empty', [], [])]

    monkeypatch.setattr(os, 'walk', walk)


def test_load_matches_images(monkeypatch):
    # type: (object) -> None
    calls = []  # type: list
    fake_walk(monkeypatch, ['spam_00.sparseimage', 'spam_01.sparseimage', 'eggs_00.sparseimage', 'README'])

    def output(command, shell):
        # type: (str, bool) -> str
        calls.append(command)
        return ''

    monkeypatch.setattr(subprocess, 'check_output', output)
    args = main.get_parser().parse_args(['load', 'spam'])  # type: argparse.Namespace
    args.func(args)
    assert calls == ['hdiutil attach -nomount  /images/spam_00.sparseimage',
                     'hdiutil attach -nomount  /images/spam_01.sparseimage',
                     'sudo zpool import spam']


def test_load_multiple_pools_preserves_current_prefix_mutation(monkeypatch, capsys):
    # type: (object, object) -> None
    fake_walk(monkeypatch, ['spam_00.sparseimage', 'eggs_00.sparseimage'])
    args = main.get_parser().parse_args(['load', '-n', 'spam', 'eggs'])  # type: argparse.Namespace
    load.load_command(args)
    output = capsys.readouterr().out  # type: str
    assert '/images/spam_00.sparseimage' in output
    assert '/images/eggs_00.sparseimage' not in output
    assert '# sudo zpool import spam\n# sudo zpool import eggs\n' in output


@pytest.mark.parametrize('failure,message', [
    ('hdiutil attach', 'Unable to attach image'),
    ('sudo zpool import', 'Unable to import zpool'),
])
def test_load_failures(monkeypatch, capsys, failure, message):
    # type: (object, object, str, str) -> None
    calls = []  # type: list
    fake_walk(monkeypatch, ['spam_00.sparseimage'])

    def output(command, shell):
        # type: (str, bool) -> str
        calls.append(command)
        if command.startswith(failure):
            raise subprocess.CalledProcessError(2, command)
        return ''

    monkeypatch.setattr(subprocess, 'check_output', output)
    args = main.get_parser().parse_args(['load', 'spam'])  # type: argparse.Namespace
    with pytest.raises(SystemExit) as error:
        args.func(args)
    assert error.value.code == 1
    assert message in capsys.readouterr().out
    assert calls[-1].startswith(failure)
