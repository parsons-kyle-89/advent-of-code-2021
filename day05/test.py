from . import main


def test_my_range() -> None:
    assert list(main.my_range(1, 5)) == [1, 2, 3, 4, 5]


def test_my_range_backwards() -> None:
    assert list(main.my_range(5, 1)) == [5, 4, 3, 2, 1]


def test_main() -> None:
    main.main()
