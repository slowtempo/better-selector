# BetterSelector

A simple, interactive terminal selection system for Python.

## Quick Start
Ensure you have `rich` installed:


pip install rich
Usage
Single Selection
Use selection to have the user pick exactly one item.

Python
import betterselector

# Returns the selected string
result = betterselector.selection("Choose one AI", ["openai", "claudecode"])
Output:

Plaintext
♦ Choose one AI
 │ ○ openai
 │ ● claudecode
Multi-Selection
Use multi_selection to allow the user to toggle multiple items using the Space key.

Python
import betterselector

# Returns a list of selected strings
results = betterselector.multi_selection("Select Tasks to Execute", ["Deploy", "Test", "Clean"])
Output:

Plaintext



♦ Select Tasks to Execute: (Space: Toggle, Enter: Done)

  [ ] Deploy
  [x] Test
❯ [x] Clean
  [x] Generate Docs
Controls
Up / Down (or k / j): Navigate the list


Space: Toggle selection

Enter: Confirm selection

q: Quit
