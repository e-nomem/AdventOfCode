import pytest

from .utils import load


def test_load_empty_string() -> None:
    p = load("")
    assert len(p) == 0


def test_load_bad_input() -> None:
    with pytest.raises(ValueError):
        load("f00")


def test_load_default_value() -> None:
    p = load("")

    assert len(p) == 0
    assert p[0] == 0
    assert p[1000] == 0


def test_load_sequential() -> None:
    s = "1,2,3,4,5,6"
    p = load(s)

    assert len(p) == 6
    for i in range(6):
        assert p[i] == i + 1
