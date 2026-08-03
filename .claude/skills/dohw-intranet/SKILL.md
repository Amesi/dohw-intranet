```markdown
# dohw-intranet Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill covers the development patterns and conventions used in the `dohw-intranet` Python codebase. It provides guidance on file naming, import/export styles, commit patterns, and testing approaches. While no specific frameworks or automated workflows are detected, this skill will help you contribute code that aligns with the project's established practices.

## Coding Conventions

### File Naming
- Use **camelCase** for file names.
  - Example: `userProfile.py`, `dataFetcher.py`

### Import Style
- Use **relative imports** within the codebase.
  - Example:
    ```python
    from .utils import calculateSum
    ```

### Export Style
- Use **named exports** (explicitly define what is exported from a module).
  - Example:
    ```python
    def fetchData():
        pass

    __all__ = ['fetchData']
    ```

### Commit Patterns
- Follow **conventional commit** style.
- Use the `feat` prefix for new features.
- Commit messages are concise (average 85 characters).
  - Example:
    ```
    feat: add user authentication to intranet portal
    ```

## Workflows

_No automated workflows detected in this repository._

## Testing Patterns

- Test files follow the pattern: `*.test.*`
  - Example: `userProfile.test.py`
- Testing framework is **unknown**; check existing test files for structure.
- Place test files alongside the modules they test or in a dedicated test directory.

### Example Test File
```python
# userProfile.test.py

from .userProfile import getUserName

def test_getUserName():
    assert getUserName(1) == "Alice"
```

## Commands
| Command | Purpose |
|---------|---------|
| /test   | Run all test files matching `*.test.*` pattern |
| /commit | Make a conventional commit with `feat` prefix |
```
