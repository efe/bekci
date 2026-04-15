# bekci

![bekci](images/bekci.png)

`bekci` is a Flake8 plugin for Python linter rules.

## Installation

Install the package in the same environment as Flake8:

```bash
pip install bekci
```

## Rules

### BEK001

Use keyword arguments when calling a function with multiple arguments.

```python
# valid
save(user)
save(user=user, force=True)

# invalid
save(user, True)
save(user, force=True)
```

## Development

Run the unit tests with:

```bash
python -m unittest discover -s tests
```
