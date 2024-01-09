from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Command:
    command_kind: str
    id: int | None = None
    value: str | None = None
    other_id: int | None = None


class History:
    def __init__(self, document: dict[int, str]) -> None:
        self._document = document
        self._history: list[CommandABC] = []
        self._pointer: int = 0

    def do(self, command: "CommandABC"):
        if command.execute(self._document, self):
            if self._pointer < len(self._history):
                self._history = self._history[: self._pointer]
            self._history.append(command)
            self._pointer += 1

    def undo(self) -> "CommandABC" | None:
        if self._pointer <= 0:
            return None
        action = self._history[self._pointer - 1]
        action.undo(self._document, self)
        self._pointer -= 1
        return action

    def redo(self) -> "CommandABC" | None:
        if self._pointer >= len(self._history):
            return None
        action = self._history[self._pointer]
        action.execute(self._document, self)
        self._pointer += 1
        return action

    def clear(self) -> None:
        self._history.clear()
        self._pointer = 0


class CommandABC(ABC):
    command_kind = ""

    @classmethod
    @abstractmethod
    def from_command(cls, command: Command) -> "CommandABC":
        raise NotImplementedError

    @classmethod
    def verify_kind(cls, command: Command):
        assert command.command_kind == cls.command_kind, "Wrong command kind"

    @abstractmethod
    def execute(self, document: dict[int, str], history: History) -> bool:
        raise NotImplementedError

    @abstractmethod
    def undo(self, document: dict[int, str], history: History):
        raise NotImplementedError


class UndoableCommand(CommandABC):
    def __init__(self) -> None:
        self._undo_action: CommandABC | None = None

    @abstractmethod
    def _execute_impl(self, document: dict[int, str], history: History) -> CommandABC | None:
        raise NotImplementedError

    def execute(self, document: dict[int, str], history: History) -> bool:
        if undo := self._execute_impl(document, history):
            self._undo_action = undo
        return bool(undo)

    def undo(self, document: dict[int, str], history: History):
        assert self._undo_action is not None, "Action must be performed, and must have made a change to be undone"
        self._undo_action.execute(document, history)


class InsertCommand(UndoableCommand):
    command_kind = "insert"

    def __init__(self, id: int, value: str):
        super().__init__()
        self._id = id
        self._value = value

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        assert command.id is not None, "Id is required"
        assert command.value is not None, "Value is required"
        return cls(command.id, command.value)

    def _execute_impl(self, document: dict[int, str], history: History):
        if self._id in document:
            return None
        document[self._id] = self._value
        return DeleteCommand(self._id)


class UpdateCommand(UndoableCommand):
    command_kind = "update"

    def __init__(self, id: int, value: str):
        super().__init__()
        self._id = id
        self._value = value

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        assert command.id is not None, "Id is required"
        assert command.value is not None, "Value is required"
        return cls(command.id, command.value)

    def _execute_impl(self, document: dict[int, str], history: History):
        if self._id not in document:
            return None
        undo = UpdateCommand(self._id, document[self._id])
        document[self._id] = self._value
        return undo


class DeleteCommand(UndoableCommand):
    command_kind = "delete"

    def __init__(self, id: int):
        super().__init__()
        self._id = id

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        assert command.id is not None, "Id is required"
        return cls(command.id)

    def _execute_impl(self, document: dict[int, str], history: History):
        if self._id not in document:
            return None
        undo = InsertCommand(self._id, document[self._id])
        del document[self._id]
        return undo


class MergeCommand(UndoableCommand):
    command_kind = "merge"

    def __init__(self, id: int, other_id: int):
        super().__init__()
        self._id = id
        self._other_id = other_id

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        assert command.id is not None, "Id is required"
        assert command.other_id is not None, "Other Id is required"
        return cls(command.id, command.other_id)

    def _execute_impl(self, document: dict[int, str], history: History):
        if self._id not in document or self._other_id not in document:
            return None
        undo = SplitCommand(self._id, self._other_id)
        document[self._id] = " ".join([document[self._id], document[self._other_id]])
        del document[self._other_id]
        return undo


class SplitCommand(UndoableCommand):
    command_kind = "split"

    def __init__(self, id: int, other_id: int):
        super().__init__()
        self._id = id
        self._other_id = other_id

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        assert command.id is not None, "Id is required"
        assert command.other_id is not None, "Other Id is required"
        return cls(command.id, command.other_id)

    def _execute_impl(self, document: dict[int, str], history: History):
        if self._id not in document or self._other_id in document or " " not in document[self._id]:
            return None
        undo = MergeCommand(self._id, self._other_id)
        document[self._id], document[self._other_id] = document[self._id].split(" ", 1)
        return undo


class MoveCommand(UndoableCommand):
    command_kind = "move"

    def __init__(self, id: int, other_id: int):
        super().__init__()
        self._id = id
        self._other_id = other_id

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        assert command.id is not None, "Id is required"
        assert command.other_id is not None, "Other Id is required"
        return cls(command.id, command.other_id)

    def _execute_impl(self, document: dict[int, str], history: History):
        if self._id not in document or self._other_id in document:
            return None
        document[self._other_id] = document[self._id]
        del document[self._id]
        return MoveCommand(self._other_id, self._id)


class CompositeCommand(CommandABC):
    def __init__(self, commands: list[CommandABC]) -> None:
        super().__init__()
        self._commands = commands

    @classmethod
    def from_command(cls, command: Command) -> CommandABC:
        raise Exception("Cannot be created from command")

    def execute(self, document: dict[int, str], history: History):
        any_effect = False
        for command in self._commands:
            if command.execute(document, history):
                any_effect = True
        return any_effect

    def undo(self, document: dict[int, str], history: History):
        for command in reversed(self._commands):
            command.undo(document, history)


class RollbackCommand(UndoableCommand):
    command_kind = "rollback"

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        return cls()

    def _execute_impl(self, document: dict[int, str], history: History):
        rolled_back_commands = []
        while command := history.undo():
            rolled_back_commands.append(command)

        return CompositeCommand(rolled_back_commands) if rolled_back_commands else None


class CommitCommand(CommandABC):
    command_kind = "commit"

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        return cls()

    def execute(self, document: dict[int, str], history: History) -> bool:
        history.clear()
        return False

    def undo(self, document: dict[int, str], history: History):
        return


class UndoCommand(CommandABC):
    command_kind = "undo"

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        return cls()

    def execute(self, document: dict[int, str], history: History) -> bool:
        history.undo()
        return False

    def undo(self, document: dict[int, str], history: History):
        return


class UpsertCommand(UndoableCommand):
    command_kind = "upsert"

    def __init__(self, id: int, value: str):
        super().__init__()
        self._id = id
        self._value = value

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        assert command.id is not None, "Id is required"
        assert command.value is not None, "Value is required"
        return cls(command.id, command.value)

    def _execute_impl(self, document: dict[int, str], history: History):
        undo: CommandABC
        if self._id in document:
            undo = UpdateCommand(self._id, document[self._id])
        else:
            undo = DeleteCommand(self._id)
        document[self._id] = self._value
        return undo


class ClearCommand(UndoableCommand):
    command_kind = "clear"

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        return cls()

    def _execute_impl(self, document: dict[int, str], history: History):
        if not any(document):
            return None
        undo = CompositeCommand([InsertCommand(key, item) for key, item in document.items()])
        document.clear()
        return undo


class RedoCommand(CommandABC):
    command_kind = "redo"

    @classmethod
    def from_command(cls, command: Command):
        cls.verify_kind(command)
        return cls()

    def execute(self, document: dict[int, str], history: History) -> bool:
        history.redo()
        return False

    def undo(self, document: dict[int, str], history: History):
        return


def execute_commands(commands: list[Command]):
    document: dict[int, str] = {}

    history = History(document)

    command_classes: list[type[CommandABC]] = [
        InsertCommand,
        UpdateCommand,
        DeleteCommand,
        MergeCommand,
        SplitCommand,
        MoveCommand,
        CommitCommand,
        RollbackCommand,
        UndoCommand,
        RedoCommand,
        ClearCommand,
    ]

    for command in commands:
        command_instance = next(
            (
                command_class.from_command(command)
                for command_class in command_classes
                if command.command_kind == command_class.command_kind
            ),
            None,
        )
        if command_instance is None:
            raise ValueError(f"Unknown command: {command}")
        history.do(command_instance)

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
