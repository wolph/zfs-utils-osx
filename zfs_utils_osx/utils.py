import subprocess


def execute(context, command, *args):
    command = ' '.join(command.split())
    context['extra_args'] = ' '.join(args)
    command %= context
    print '#', command
    if not context['no_op']:
        return subprocess.check_output(command, shell=True)


def coalesce(*arg):
    return reduce(lambda x, y: x if x is not None else y, arg)

