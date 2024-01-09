from .command import execute_commands, Command


def test_hello_universe():
    outcome = execute_commands(
        [
            Command("insert", id=1, value="Hello"),
            Command("insert", id=2, value="World"),
            Command("update", id=2, value="Universe"),
            Command("merge", id=1, other_id=2),
            Command("commit"),
            Command("insert", id=3, value="!"),
            Command("merge", id=2, other_id=3),
            Command("split", id=2, other_id=3),
            Command("insert", id=4, value="?"),
            Command("undo"),
            Command("merge", id=1, other_id=4),
            Command("merge", id=1, other_id=3),
            Command("commit"),
            Command("undo"),
            Command("insert", id=5, value="!"),
            Command("insert", id=6, value="?"),
            Command("rollback"),
            Command("split", id=1, other_id=2),
            Command("split", id=2, other_id=3),
            Command("commit"),
        ]
    )

    assert outcome == {1: "Hello", 2: "Universe", 3: "!"}


def test_undo_rollback():
    outcome = execute_commands(
        [
            Command("insert", id=1, value="Hello"),
            Command("insert", id=2, value="World"),
            Command("rollback"),
            Command("undo"),
        ]
    )

    assert outcome == {1: "Hello", 2: "World"}


def test_undo_redo():
    outcome = execute_commands(
        [
            Command("insert", id=1, value="Hello"),
            Command("undo"),
            Command("redo"),
        ]
    )

    assert outcome == {1: "Hello"}


def test_undo_redo_multiple():
    outcome = execute_commands(
        [
            Command("insert", id=1, value="Hello"),
            Command("insert", id=2, value="World"),
            Command("undo"),
            Command("undo"),
            Command("redo"),
            Command("redo"),
        ]
    )

    assert outcome == {1: "Hello", 2: "World"}


def test_undo_branch():
    outcome = execute_commands(
        [
            Command("insert", id=1, value="Hello"),
            Command("insert", id=2, value="World"),
            Command("undo"),
            Command("insert", id=2, value="Universe"),
            Command("undo"),
            Command("redo"),
            Command("redo"),
        ]
    )

    assert outcome == {1: "Hello", 2: "Universe"}


def test_clear():
    outcome = execute_commands(
        [
            Command("insert", id=1, value="Hello"),
            Command("insert", id=2, value="World"),
            Command("clear"),
        ]
    )

    assert outcome == {}


def test_clear_undo():
    outcome = execute_commands(
        [
            Command("insert", id=1, value="Hello"),
            Command("insert", id=2, value="World"),
            Command("clear"),
            Command("undo"),
        ]
    )

    assert outcome == {1: "Hello", 2: "World"}

# TODO: add more tests, especially specific to individual commands and new commands (e.g. undo upsert)