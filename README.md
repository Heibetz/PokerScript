# PokerScript (Stacked)

PokerScript is a stack-based esoteric programming language where every instruction is a poker term. Programs are written in `.nlh` files (No-Limit Hold'em) and executed by the `poker.py` interpreter.

## Running a Program

```
python poker.py <filename>
```

For example:

```
python poker.py examples/helloworld.nlh
```

## How It Works

PokerScript operates on a **stack** — a last-in, first-out (LIFO) data structure. Think of it like a stack of poker chips: you can only add to or remove from the top. Every instruction either pushes values onto the stack, pops values off it, or moves values around within it.

The interpreter reads the program file line by line. Each line is one instruction. Blank lines and lines starting with `#` are ignored. A **program counter** (pc) tracks which line is currently being executed and advances by one after each instruction, unless a jump occurs.

All values on the stack are integers. Characters are represented by their ASCII codes (e.g., `72` = `H`, `101` = `e`).

## Instruction Set

| Instruction | Description |
|-------------|-------------|
| `ANTE`      | Push `0` onto the stack. |
| `RAISE`     | Pop the top value, add `1`, and push the result back. Used for incrementing values. |
| `BET n`     | Lyrics lookup. Pushes the ASCII value of the character at position `n` in `kennyrogers.txt`. This is the primary way to push specific characters onto the stack. |
| `CALL`      | Duplicate the top value. Pops it, then pushes it back twice, so the stack ends up with two copies. |
| `FOLD`      | Subtraction. Pops `A` (top), then pops `B` (second), and pushes `B - A`. |
| `DEAL`      | Read one line of input. Pushes the ASCII code of the first character. If input is empty or exhausted, pushes `0`. |
| `SHOW`      | Pop the top value and print it as a character (using its ASCII code). |
| `STACK`     | Pop the top value and print it as an integer. |
| `ALLIN n`   | Conditional jump. Pops the top value — if it is `0`, jumps to line `n`. If it is not `0`, execution continues normally. Lines are **1-indexed**. |
| `CUT`       | Move the top of the stack to the bottom. Pops the top value and inserts it at the very bottom of the stack. |
| `SHUFFLE`   | Move the bottom of the stack to the top. Removes the bottom-most value and pushes it on top. |
| `BUST`      | End the program immediately. |

### Key Concepts

- **Building numbers with `BET`:** `BET n` looks up the character at position `n` in `kennyrogers.txt` and pushes its ASCII code. For example, position 239 is `H` (ASCII 72), so `BET 239` pushes `72`. If the character you need isn't in the lyrics, use `BET` to get a nearby value and `RAISE` to increment to it (e.g., `BET 6` pushes 32, then `RAISE` makes it 33 = `!`).
- **Incrementing with `RAISE`:** `RAISE` pops the top value, adds 1, and pushes the result. Useful for fine-tuning values after a `BET`, or for arithmetic in loops.
- **Conditional jumps:** `ALLIN n` is the only form of control flow. It pops and checks the top value — jumping to line `n` only when the value is zero.
- **Unconditional jumps:** Push `0` with `ANTE`, then immediately `ALLIN n`. Since the top is guaranteed to be `0`, the jump always fires.
- **Stack rotation:** `CUT` and `SHUFFLE` let you access values buried in the stack without losing them. `CUT` sends the top to the bottom; `SHUFFLE` brings the bottom to the top.

---

## Examples

### cat.nlh — Echo (Cat Program)

```
DEAL
CALL
SHOW
ALLIN 1
```

This program reads one character at a time and echoes it back, looping until the input is exhausted.

**Step-by-step:**

1. **`DEAL`** — Read a character from input and push its ASCII code. If there is no input, pushes `0`.
2. **`CALL`** — Duplicate the top value. The stack now has two copies of the character.
3. **`SHOW`** — Pop one copy and print it as a character.
4. **`ALLIN 1`** — Pop the other copy. If it is `0` (meaning input was exhausted), jump to line 1, which reads again and will get `0` again, eventually ending. If it is not `0`, execution continues to line 1 anyway (since line 4 is the last line, pc advances past the end and the program finishes — but the jump on `0` actually loops back to keep reading).

In practice: type a character, press Enter, and the program prints it back. Repeat until you send an empty line.

---

### reversestring.nlh — Reverse a String

```
DEAL        Line 1
CALL        Line 2
ALLIN 7     Line 3
ANTE        Line 4
ALLIN 1     Line 5
            Line 6 (blank)
CUT         Line 7
CALL        Line 8
ALLIN 13    Line 9
SHOW        Line 10
ANTE        Line 11
ALLIN 8     Line 12
```

This program reads characters one at a time, then prints them in reverse order.

**Phase 1 — Read input (lines 1–5):**

1. **`DEAL`** — Read a character.
2. **`CALL`** — Duplicate it.
3. **`ALLIN 7`** — Pop the duplicate. If it was `0` (empty input), jump to Phase 2 at line 7. Otherwise, continue.
4. **`ANTE`** — Push `0`.
5. **`ALLIN 1`** — Pop the `0`, which triggers an unconditional jump back to line 1 to read the next character.

After this phase, the stack holds all the input characters with the first character at the bottom and the last at the top (plus a trailing `0` from the final empty `DEAL`).

**Phase 2 — Print reversed (lines 7–12):**

7. **`CUT`** — Move the trailing `0` from the top to the bottom of the stack. This `0` now serves as a sentinel to detect when all characters have been printed.
8. **`CALL`** — Duplicate the top character.
9. **`ALLIN 13`** — Pop the duplicate. If `0` (sentinel reached), jump to line 13 which is past the end, so the program stops. Otherwise, continue.
10. **`SHOW`** — Pop and print the character.
11. **`ANTE`** — Push `0`.
12. **`ALLIN 8`** — Unconditional jump back to line 8.

Since the stack is LIFO, popping characters off the top naturally reverses the input order.

**Example run:**

```
$ python poker.py examples/reversestring.nlh
r
a
c
e
c
a
r
            ← (empty line to finish input)
racecar
```

---

### repeater.nlh — Repeat a Character N Times

```
Lines 1–49:   ANTE followed by 48 RAISEs  → pushes 48 (ASCII '0')
Line 50:      (blank)
Line 51:      DEAL                         → read the character to repeat
Line 52:      DEAL                         → read the count (as a character like '5')
Line 53:      SHUFFLE                      → bring 48 from the bottom to the top
Line 54:      FOLD                         → subtract 48 from the count character's ASCII code
Line 55:      (blank)
Line 56:      CALL                         → duplicate the counter
Line 57:      ALLIN 69                     → if counter is 0, jump past the end → stop
Line 58:      (blank)
Line 59:      ANTE                         → push 0
Line 60:      RAISE                        → push 1
Line 61:      FOLD                         → subtract 1 from the counter (decrement)
Line 62:      (blank)
Line 63:      SHUFFLE                      → bring the character from the bottom to the top
Line 64:      CALL                         → duplicate the character
Line 65:      SHOW                         → print the character
Line 66:      SHUFFLE                      → (cycle stack to restore order)
Line 67:      ANTE                         → push 0
Line 68:      ALLIN 55                     → unconditional jump back to the loop check
```

**How it works:**

The program first builds the value `48` on the stack (the ASCII code of `'0'`). This is used to convert a digit character to its numeric value — for instance, `'5'` has ASCII code `53`, and `53 - 48 = 5`.

It then reads two inputs: the character to repeat and the repetition count (a single digit). It subtracts `48` from the count's ASCII code to get the actual number.

The main loop duplicates the counter and checks if it's `0` (done). If not, it decrements the counter by `1`, brings the character to the top, duplicates and prints it, then loops back.

**Example run:**

```
$ python poker.py examples/repeater.nlh
a
7
aaaaaaa
```

---

### helloworld.nlh — Hello, World!

```
BET 239    → H
SHOW
BET 2      → e
SHOW
BET 86     → l
SHOW
BET 86     → l
SHOW
BET 37     → o
SHOW
BET 89     → ,
SHOW
BET 6      → (space)
SHOW
BET 15     → w
SHOW
BET 37     → o
SHOW
BET 3      → r
SHOW
BET 86     → l
SHOW
BET 52     → d
SHOW
BET 6      → (space, ASCII 32)
RAISE      → 32 + 1 = 33 = !
SHOW
```

This program prints `Hello, world!` using `BET` to look up each character from `kennyrogers.txt`. Each `BET n` pushes the ASCII code of the character at position `n` in the lyrics, and `SHOW` prints it.

The only character not directly in the lyrics is `!` (ASCII 33). To get it, we use `BET 6` (space = 32) followed by a bare `RAISE` to increment it to 33.

**Example run:**

```
$ python poker.py examples/helloworld.nlh
Hello, world!
```