# Pytest (Parametrize) Suite

A tiny plugin for writing clean, easy-to-read, parametrized tests in pytest.

## Why?

Pytest's `parametrize` is a powerful way to write input-output testing to rapidly 
expand your test coverage while minimizing the number of test assertions you must 
write. Unfortunately, as the complexity of your test suite grows, it can become 
difficult to keep track of individual test cases.

One way to get cleaner test output is by assigning descriptive `ids` and `argnames` to 
each parametrized case. However, the current methodologies available result in either 
very verbose setup, or difficult-to-track ids and names.

Enter `pytest-parametrize-suite`. With this marker, you define your test ids and 
names in-line with the values you intend to pass into your test, keeping your 
identifiers tightly coupled to your test cases and encouraging a delightful testing 
experience as a result.

## Quickstart

### Install With PIP

```shell
pip install -U pytest-parametrize-suite
```

### Install With Poetry

```shell
poetry add --group=test pytest-parametrize-suite
```

## Using the plugin

The plugin provides a single entrypoint in a pytest marker called `suite`. 

The `suite`
marker takes any number of keyword arguments. Each entry in should be a Mapping of 
`argname->argvalue` and all entries should be the same exact shape.

This gives developers the ability to 

#### Example

**Given the following module:**

```python
# iso8601.py

from __future__ import annotations

import datetime


def iso8601(
    date_obj: datetime.date | datetime.datetime | datetime.time | datetime.timedelta
) -> str:
    """Format a Python date/time object into an ISO8601 string."""

    if isinstance(date_obj, (datetime.date, datetime.time)):
        return date_obj.isoformat()
    if isinstance(date_obj, datetime.timedelta):
        return timedelta_isoformat(date_obj)
    raise ValueError(
        f"Unrecognized value of type: {date_obj.__class__.__name__}: {date_obj}"
    )


def timedelta_isoformat(delta: datetime.timedelta) -> str:
    """Why isn't this part of the stdlib?"""
    usecs = abs(
        (delta.days * 24 * 60 * 60 + delta.seconds) * 1000000 + delta.microseconds
    )
    seconds, usecs = divmod(usecs, 1000000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    fmt = f"P{days}DT{hours}H{minutes}M{seconds}.{usecs:06}S"
    return fmt

```

**Writing With pytest-parametrize-suite:**

```python
# test_iso8601.py

from __future__ import annotations

import datetime

import pytest

from example.iso8601 import iso8601


@pytest.mark.suite(
    datetime=dict(
        given_date_obj=datetime.datetime(1970, 1, 1),
        expected_date_str="1970-01-01T00:00:00",
    ),
    date=dict(
        given_date_obj=datetime.date(1970, 1, 1),
        expected_date_str="1970-01-01",
    ),
    time=dict(
        given_date_obj=datetime.time(),
        expected_date_str="00:00:00",
    ),
    timedelta=dict(
        given_date_obj=datetime.timedelta(1, 1, 1),
        expected_date_str="P1DT1.000001S",
    )
)
def test_iso8601(given_date_obj, expected_date_str):
    # When
    date_str = iso8601(given_date_obj)
    # Then
    assert date_str == expected_date_str

```

**Writing Without pytest-parametrize-suite:**

```python
# test_iso8601.py

from __future__ import annotations

import datetime

import pytest

from example.iso8601 import iso8601


@pytest.mark.parametrize(
    argnames=("given_date_obj", "expected_date_str"),
    argvalues=[
        (datetime.datetime(1970, 1, 1), "1970-01-01T00:00:00"),
        (datetime.date(1970, 1, 1), "1970-01-01"),
        (datetime.time(), "00:00:00"),
        (datetime.timedelta(1, 1, 1), "P1DT1.000001S")
    ],
    ids=["datetime", "date", "time", "timedelta"]
)
def test_iso8601(given_date_obj, expected_date_str):
    # When
    date_str = iso8601(given_date_obj)
    # Then
    assert date_str == expected_date_str

```

Running the test defined in the example outputs the following:

```shell
❯ pytest test_iso8601.py -v
=============================== test session starts ===============================
platform darwin -- Python 3.11.0, pytest-7.2.1, pluggy-1.0.0 -- /Users/god/Library/Caches/pypoetry/virtualenvs/pytest-parametrize-suite-TGMGi3Zp-py3.11/bin/python
cachedir: .pytest_cache
rootdir: /Users/god/PycharmProjects/pytest-parametrize-suite
plugins: parametrize-suite-23.1.0, cov-4.0.0
collected 4 items                                                                 

src/pytest_parametrize_suite/example.py::test_iso8601[datetime] PASSED      [ 25%]
src/pytest_parametrize_suite/example.py::test_iso8601[date] PASSED          [ 50%]
src/pytest_parametrize_suite/example.py::test_iso8601[time] PASSED          [ 75%]
src/pytest_parametrize_suite/example.py::test_iso8601[timedelta] PASSED     [100%]

================================ 4 passed in 0.02s ================================
```

As you can see, we get a developer-friendly output for our parametrized tests while 
minimizing the amount of cognitive overhead it takes to understand and develop our test 
cases.

Happy testing! :white_check_mark:
