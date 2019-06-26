import os
import dotbot
import subprocess


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


class Go(dotbot.Plugin):
    """
    Installs GoLang tools by using 'go get' command
    """

    _directive = 'go'

    _default_values = {
        'package': '',
        'flags': [],
        'stdin': False,
        'stdout': False,
        'stderr': False,
    }

    _go_exec = which('go')

    def can_handle(self, directive):
        return directive == self._directive and self._go_exec

    def handle(self, directive, data):
        if not self.can_handle(directive):
            raise ValueError(
                'Can not handle directive %s or go no installed' % directive
            )
        success = True
        for pkg_info in data:
            data = self._apply_defaults(pkg_info)

            success &= self._handle_single_package(data) == 0
        if not success:
            self._log.warning('Not all packages installed.')
        else:
            self._log.info('Finished installing go packages')
        return success

    def _handle_single_package(self, data):
        package = data.get('package', '')
        if not package:
            return 0
        with open(os.devnull, 'w') as devnull:
            stdin = None if data.get('stdin', False) else devnull
            stdout = None if data.get('stdout', False) else devnull
            stderr = None if data.get('stderr', False) else devnull

            flags = data.get('flags', [])

            cmd = [self._go_exec, 'get'] + flags + [package]
            self._log.warning('Running command: %s' % ' '.join(cmd))
            ret = subprocess.call(
                cmd,
                shell=False,
                stdout=stdout,
                stderr=stderr,
                stdin=stdin,
                cwd=self._context.base_directory(),
            )
            return ret

    def _apply_defaults(self, data):
        defaults = self._context.defaults().get('go', {})
        base = {
            key: defaults.get(key, value) for key, value in self._default_values.items()
        }

        if isinstance(data, dict):
            base.update(data)
        else:
            base.update({'package': data})

        return base
