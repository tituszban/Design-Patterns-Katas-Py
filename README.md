# Design Patterns Katas \[Py\]

Welcome to this repository of refactoring exercises (or Katas). The goal of each of these exercises is to learn about [Design Patterns](https://en.wikipedia.org/wiki/Software_design_pattern) by taking a semi-realistic example and improving it using one of the Design Patterns.

Each of the folders within [exercises](./exercises/) contains one folder with the exercise setup, and a README with more details. To see an example solution, try the [`solutions` branch]()

## Who are these exercises for?

These exercises are designed for any software engineer looking to learn about and/or practice design patterns. The goal is to make each of them reasonably beginner friendly, however, they should offer enough of a challenge for more seasoned developers.

## Knowledge prerequisits

Although these exercises are aimed at less experienced developers, there are some requirements to be able to meaningfully complete the exericses. Understanding of object oriented programming is needed. And as this repo is in Python, you also need to know Python. Also, some knowledge of regular expressions is recommended for some of the exercises. But not crucial. If you don't understand something, [Regex101](https://regex101.com/) can probably help you.

The code is also using type hints. If you are not familiar with these, or don't want to bother, just ignore/delete them.

## Code prerequisits

Python 3.12 or higher. It may work on lower versions, but I have not tested those.

## Setup

1. _\[Optional\]_ Star this repository. This is not needed, but is highly apprechiated!
2. Fork this repository using the Fork button on GitHub. This creates your own copy of this repo, so you can push to it
3. Clone your fork of the repository
4. Install requirements
```
pip install -r requirements.txt
```
or on Linux
```
pip3 install -r requirements.txt
```
5. _\[Optional\]_ Create a branch for your attempt. This is not needed, but it may help with keeping track and reverting your changes.
6. _\[Optional\]_ Install [Ruff](https://github.com/astral-sh/ruff) ([VSCode extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)). Formatting and static analysis is configured for Ruff.

That is it.

## Some help for the exercises

Although each exercise spec is described in their relevant README, they are meant to be difficult to read and understand. Think about this as legacy code you came across. Before you start refactoring, you probably want to read and understand the code. Maybe even add comments if that helps.

Then you probably want to add unit tests. Each folder will have an empty pytest file setup. Consider adding a number of cases to validate if your code still works the same, or if it regressed while you were changing it. The point of refactoring, is to change the internal code structure, without changing the output. (You can chose to change the output if you like, but it will make it harder to automate comparisons and regression testing. Do so at your own risk.)

Then start changing code. Read about the pattern, and try to figure out how it can be applied to the code. It may take multiple attempts to get code you are happy with. This is normal, even expected. Feel free to use git to its fullest, branch to try out ideas, abandon them, roll back, etc.

Remember, the point of design patterns isn't to make code more terse. The point is to make it:
 - Easier to read and understand
 - Easier to extend
 - Easier to test

You are likely going to end up with more code by the end then before, and that is just fine. The goal is to write code that you are happy with, and learn something along the way.

Each exercise will also include challenges of various difficulty. If you can't do the harder things, don't feel bad. Feel free to come back to them later. Similarly, each exercise will include some hints. Feel free to use them.

And finally, if you have done an exercise, you may want to think about what other design patterns you could apply to it.

## Run your code

There are a number of different ways you can run each exercise. All of them are designed to print out some meaningful text, you can compare and validate manually, if you don't want to write unit tests. Also, each of them will have a function you can write your own input for the same reason.

You can run the module level command and pick an exercise. So for example, to run the composite exercise:

```
python -m exercises composite
```

You can also run each of the files indidually:
```
python ./exercises/composite/composite.py
```

Or, you may chose to write unit tests, and run those:

```
pytest .\exercises\composite\
```

## Feedback and contribution

Feedback is welcome please feel free to raise an issue to discuss any of the exercises.

If you would like to contribute challenges, please raise an issue with your ideas to discuss it. Or, just open a Pull Request.

If you would like to contribute by translating the challenges into other languages (both programming and human), there will be repos coming for other (programming) languages, and feel free to add `README.[lang].md` files to any of the exercises.
