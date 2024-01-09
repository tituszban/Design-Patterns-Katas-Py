from dataclasses import dataclass



# Models:
# You may not modify these models, as theoretical systems outside this exercise expect to use these models to communicate with your method
@dataclass
class Command:
    command_kind: str
    id: int | None = None
    value: str | None = None
    other_id: int | None = None


def execute_commands(commands: list[Command]) -> dict[int, str]:
    document: dict[int, str] = {}

    history: list[dict[int, str]] = [document.copy()]
    last_commit = 0

    for command in commands:
        if command.command_kind == "insert":
            assert command.id is not None, "Missing id"
            assert command.value is not None, "Missing value"
            if command.id in document:
                continue
            document[command.id] = command.value
        elif command.command_kind == "update":
            assert command.id is not None, "Missing id"
            assert command.value is not None, "Missing value"
            if command.id not in document:
                continue
            document[command.id] = command.value
        elif command.command_kind == "delete":
            assert command.id is not None, "Missing id"
            if command.id not in document:
                continue
            del document[command.id]
        elif command.command_kind == "merge":
            assert command.id is not None, "Missing id"
            assert command.other_id is not None, "Missing other id"
            if command.id not in document or command.other_id not in document:
                continue
            document[command.id] = ' '.join([document[command.id], document[command.other_id]])
            del document[command.other_id]
        elif command.command_kind == "split":
            assert command.id is not None, "Missing id"
            assert command.other_id is not None, "Missing other id"
            if command.id not in document or command.other_id in document or ' ' not in document[command.id]:
                continue
            document[command.id], document[command.other_id] = document[command.id].split(" ", 1)
        elif command.command_kind == "move":
            assert command.id is not None, "Missing id"
            assert command.other_id is not None, "Missing other id"
            if command.id not in document or command.other_id in document:
                continue
            document[command.other_id] = document[command.id]
        elif command.command_kind == "commit":
            last_commit = len(history) - 1
            continue
        elif command.command_kind == "rollback":
            document = history[last_commit]
            while len(history) > last_commit:
                history.pop(-1)
            continue
        elif command.command_kind == "undo":
            if len(history) < 2 or len(history) - 1 <= last_commit:
                continue
            document = history[-2]
            history.pop(-1)
            continue
        else:
            raise ValueError(f"Unknown command: {command}")
        history.append(document.copy())

    return document


def run_example():
    example = [
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

    print(f"Example: {example}")
    document = execute_commands(example)
    print(f"Document: {document}")


if __name__ == "__main__":
    run_example()
