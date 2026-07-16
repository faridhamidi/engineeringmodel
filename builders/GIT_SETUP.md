<!--
Type: Builder surface (prerequisite)
Status: implemented
Origin: .meta/builder-accessible-layer.design.md section 3.3
Owner: repository maintainer (assign on adoption)
Evidence: commands are documented; installation on every platform is not demonstrated.
-->

# Git Setup

Git supplies the local save points used by the builder layer. You need both the git
program and a project initialized as a git repository.

## Install Git

### macOS

Use Apple's command-line tools:

```bash
xcode-select --install
```

Or, with Homebrew:

```bash
brew install git
```

### Windows

Use Windows Package Manager:

```powershell
winget install --id Git.Git -e
```

The Git for Windows installer is an equivalent option.

### Ubuntu Or Debian

```bash
sudo apt update
sudo apt install git
```

### Fedora

```bash
sudo dnf install git
```

## Verify And Initialize

Verify the installation:

```bash
git --version
```

From the project directory, initialize version history when it is not already a git
repository:

```bash
git init
```

Do not initialize inside another project's repository without understanding which
directory should own the history. Before the first commit, exclude credentials,
private runtime data, generated output, and other material that should not enter
version history.

Git protects local authoring. It does not reverse an effect already applied to a shared
or external system; follow [Safe Operation](SAFE_OPERATION.md) before such an action.
