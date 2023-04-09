# Gester

A game engine for console based text game

```
$ gest gernards_tale.gest

Enter your player name: Alex
Hello Alex. Welcome to Gernard's Tale

You are about to enter a mistic and eerie world, full of wonders
that will unfold before your eyes. Your progress will be saved
automatically

Are you ready to proceed? (y/n): n
```

The above gameplay is bought about by a game script `gernards_tale.gest`
which look like:

```
[input: name] Enter you player name:
Hello {name}. Welcome to Gernard's Tale

You are about to enter a mistic and eerie world, full of wonders
that will unfold before your eyes. Your progress will be saved
automatically

[yes_or_no: p] Are you ready to proceed?
[{p} no]
  [abort]
[endblock]

  ...
```

Gest command will invoke the game engine which will read the game
script file (.gest file) and present the game on the command window
