import pytest

from .lib import window


def test_window_empty_iterable() -> None:
    it = window([])  # type: ignore

    with pytest.raises(StopIteration):
        next(it)


def test_single_window() -> None:
    it = window([0, 1])

    result = [i for i in it]

    assert result == [(0, 1)]


def test_multiple_windows() -> None:
    it = window(range(5))

    result = list(i for i in it)

    assert result == [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
    ]


@pytest.mark.parametrize(
    'window_size', [
        0,
        -1,
    ],
)
def test_window_window_size_less_than_one(window_size: int) -> None:
    with pytest.raises(ValueError) as e:
        it = window(range(5), window_size)
        # Lazy evaluation means the exception is not raised until we try to read
        # from the iterator
        next(it)

    assert str(e.value) == 'Window size must be greater than 0'


def test_window_window_size_one() -> None:
    it = window(range(5), 1)

    result = [i for i in it]

    assert result == [(i,) for i in range(5)]


def test_window_large_window_size() -> None:
    it = window(range(5), 4)

    result = list(i for i in it)

    assert result == [
        (0, 1, 2, 3),
        (1, 2, 3, 4),
    ]
