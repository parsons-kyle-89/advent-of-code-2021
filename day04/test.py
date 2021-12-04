from . import main


def default_game() -> main.Game:
    board = (
        (1, 2, 3, 4, 5),
        (6, 7, 8, 9, 10),
        (11, 12, 13, 14, 15),
        (16, 17, 18, 19, 20),
        (21, 22, 23, 24, 25),
    )
    return main.Game(board)


def test_main() -> None:
    main.main()


def test_row_won() -> None:
    game = default_game()
    for number in [1, 2, 3, 4]:
        game.mark(number)
        assert not game.won()
    game.mark(5)
    assert game.won()


def test_col_won() -> None:
    game = default_game()
    for number in [4, 9, 14, 19]:
        game.mark(number)
        assert not game.won()
    game.mark(24)
    assert game.won()
