Dotbot-golang
=============

Plugin for [dotbot](https://github.com/anishathalye/dotbot) that knows 
how to install [GoLang](https://golang.org/) packages.

Usage
-----

Add this repo as subrepo to your dotfiles and update `install` script.

```bash
git submodule add https://github.com/delicb/dotbot-golang
```

Then, modify install script to add path to `dotbot-golang` directory that you
just added. Only last line is relevant (if it was not changed from default) and
after change it might look like this:

```bash
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" -c "${CONFIG}" --plugin-dir=dotbot-golang "${@}"
```

To use it, add go directive. Values can be simple (only package name) or more
detailed (dict with flags passed to `go get` command). Example:

```yaml
- go:
  - github.com/delicb/cliware
  - package:
    - github.com/delicb/cliware-middlewares
    flags: [-v, -u]
    stdout: true
    stderr: true
```

