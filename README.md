# Feihong's Gevent Quickstart

## Installation

## Dependencies

```
brew update
brew install pypy3
```

## Project

```
pipenv --python pypy3 install
```

## References

- [PyPy - Download and install](https://pypy.org/download.html)

## Notes

At the time of writing, it is not possible to install psycopg2cffi because it is not yet compatible with Python 3.5 (which is what PyPy 5.9.0 is based on). You can't just use psycopg2 because it is not compatible with PyPy.
