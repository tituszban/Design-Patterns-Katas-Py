# Command Pattern

The Command Pattern is a Behavioural pattern first published in the Gang of Four book _Design Patterns: Elements of Reusable Object-Oriented Software_.

TODO: Write about the use cases of this pattern. In the meantime, read about the [Command Pattern of Wikipedia](https://en.wikipedia.org/wiki/Command_pattern)

## Command Pattern Exercise

In this exercise, you are implementing an analog to a key-value store, with some advanced features. Legacy code is already in place, however when a large number of commands are processed, and the more values are stored, the solution is using too much memory. Also its architecture doesn't lend itself to implementing some new features. Commands are passed in as a standard `Command` object, which you may not modify (you can, but you shouldn't really...). You must return the final state of the store document, after all the commands are executed.

### Requirements

The following commands are supported currently:

 - `insert`: Sets the `id` record to `value`. If `id` is already present, it is ignored
 - `update`: Sets the `id` record to `value`. If `id` is not already present, it is ignored
 - `delete`: Remove the record with `id`. If `id` is not already present, it is ignored
 - `merge`: Merge `id` and `other_id` into a single record, with key `id`, and the two values separated by a space. Both ids must be present, or it is ignored. The record with `other_id` is deleted.
 - `split`: Splits the `id` record, with the contents until the first space kept in `id` and the rest placed to `other_id`. If `id` is not present, or `other_id` is already present, or if there is no space in the `id` record, it is ignored
 - `move`: Move the contents of `id` to `other_id`. If `id` is missing, or `other_id` is already present, ignored.
 - `commit`: Creates a fixed point in history. It is not possible to undo the document in any way until before this point.
 - `rollback`: Undoes all changes until the last commit (or the start of the document)
 - `undo`: Undoes the last change to the document. Commands that were ignored are not considered. Changes cannot be undone to before a commit. If there are no changes, it is ignored.

If a command doesn't have all the required fields, an error is thrown.

### Your goals are

You need to make the following changes:

 - Add a new `Upsert` command, which sets the `id` record to `value`. If `id` is already present, it is updated
 - Add a new `Clear` command, which clears all record. Both of these commands can be undone.
 - Add the ability to undo a rollback command, restoring the document to before the rolled back state.
 - Add redo functionality. After an undo, if a redo is issued, the undo is undone. This holds to multiple undos and redos. Commands that didn't change the document are still not considered. If a change has been undone, and then a new change was made, it is no longer possible to undo the change and then redo the undone change (history is linear, not a tree).

While implementing these changes, also identify what could be the cause of the memory issue, when a large number of values is stored, and many commands are executed. See if you can reproduce the issue, and then fix it.

It is important, that we could add more commands, without worrying about any of the previous commands changing. It just so happens that the Command Pattern could do this exact thing, as changes, and undoing them can be encapsulated into a single object which can be added and tested by itself. It would also make the code easier to read. Consider refactoring to use this pattern first, before implementing other changes.

### Hints

<details>
  <summary>Hint 1</summary>

You need to convert the existing `Command` object, into a command implementation, such as this one:

```py
class InsertCommand:
    def __init__(self, insert_id: int, value: str) -> None:
        self._insert_id = insert_id
        self._value = value

    def execute(self, document: dict[int, str]) -> dict[int, str]:
        document[self._insert_id] = self._value
        return document
```

Note, none of the actual validation is implemented here.

</details>

<details>
  <summary>Hint 2</summary>

For each of the commands, you need to store if it made a change to the document (e.g. It is not ignored). If not, it can be discarded. If it did however, it should be stored in a history.

Each command should be independently undoable. Consider each command holding the logic to undo it, instead of storing each state. This leads to the memory issues by the way. If the command just does the original command in reverse when undone, it can simplify managing history a lot as well.

</details>

<details>
  <summary>Hint 3</summary>

Undoing the rollback requires storing all the changes the rollback made at once.

</details>

<details>
  <summary>Hint 4</summary>

When committing, you may as well discard the history, as nothing may revert the document to a state before the commit.

</details>

<details>
  <summary>Hint 5</summary>

To support the redo, you cannot discard commands that were undone. Consider using a pointer and a list, where when undone, the command at the current pointer is undone, and the pointer is moved back. Then to redo, the pointer is moved forward, and the command is executed again. If the pointer is not at the end of the list, when a new command is executed, all commands ahead of the pointer should be dropped.

</details>