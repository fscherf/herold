# herold

herold is a simple command line tool to manage additional metadata in git commits. It adds a YAML block to otherwise human-readable commit messages, which can be used to auto-generate changelogs from the git history.

**Example commit message:**

```
utils: add_numbers: fix addition of large floating point numbers

Previously, `utils.add_numbers` returned wrong results if one of the given
numbers came close to INT_MAX. This was due to a bug in the underlying math
library that `utils.add_numbers` uses.

This patch updates the math library to the newest version to fix this problem.

meta:
  flags: []

  changelog:
    revokes: []

    breaking-changes:
      - ""

    changes:
      - ""

    bug-fixes:
      - "Addition of large floating point numbers was fixed"

    chores:
      - "math-lib was updated from 0.0 to 1.0"

Signed-off-by: Florian Scherf <mail@florianscherf.de>
---
```

**Example Changelog:**

`$ herold changelog $(herold releases --as-ranges) --sections bug-fixes chores`

```markdown
# Changelog

## 0.1

### Bug Fixes
- Addition of large floating point numbers was fixed (b6a34734beba)

### Chores
- math-lib was updated from 0.0 to 1.0 (b6a34734beba)
```


## Getting Started

### Setup

```bash
$ pip install herold
$ cd ~/git/my-project
$ herold init  # sets up a herold config in `.herold`
$ herold install  # sets up a git prepare-commit-msg hook
```


### Making Commits

herold tries to extract the first YAML block of a commit message that starts
with `meta:`. When the herold git prepare-commit-msg hook is installed, this
block gets auto generated when `git commit` is called.

This can be customized by adding additional sections to the `changelog` section
of the `.herold/config.yml` file or by updating the template of the meta data
block in `.config/meta-data.yml`.


### Revoking Changelog Entries

In development it can happen that you attempt to fix something, and need to
revert the fix because it causes additional problems. To avoid duplicate lines
in the changelog, you can revoke changelog entries, using the `revoke` keyword
in the changelog block.

```yaml
The previous fix produced more problems, this is the actual fix.

meta:
  changelog:
    revokes: ["b6a34734beba"]

    bug-fix:
      "Bug was fixed"
```

### Releases

herold uses a regex pattern, defined in `.herold/config.yml` to determine which
git tags are release tags. The default pattern allows numerics and dots.
`2.0.17` would be a valid release tag.

Use `herold releases` to list all matching releases, and
`herold releases --as-ranges` as input for `herold changelog`.


### Changelogs

`herold changelog` generates changelogs from git commit ranges. By default, the
output format is markdown, which can be customized by updating the changelog
template in `.herold/changelog`.

The changelog sections in commit messages are fully customizable. By default
`herold changelog` renders the sections `breaking-changes`, `changes`, and
`bug-fixes`. To render additional or custom sections, use the `--sections`
argument.

```bash
# generates a changelog for the last 10 commits
$ herold changelog -10

# generates a changelog for all changes between the releases 0.0 and 1.0
$ herold changelog 0.0..1.0

# generates a full changelog of your project for all releases
$ herold changelog $(herold releases --as-ranges)
```


### Flags

For additional information, meta data blocks can contain flags.

```yaml
This is a confidential change.

meta:
  flags: ["confidential"]
```

```bash
# prints a list off all commits within the range `-10` that contain
# the tag `confidential`
$ herold find -10 --flags confidential
```
