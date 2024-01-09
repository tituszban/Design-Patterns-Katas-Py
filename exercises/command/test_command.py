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
