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

The interpreter reads the program file line by line. Each line is one instruction. Blank lines are skipped. A **program counter** (pc) tracks which line is currently being executed and advances by one after each instruction, unless a jump occurs.

All values on the stack are integers. Characters are represented by their ASCII codes (e.g., `72` = `H`, `101` = `e`).

## Instruction Set

| Instruction  | Description |
|--------------|-------------|
| `ANTE`       | Push `0` onto the stack. |
| `RAISE`      | Pop the top value, add `1`, and push the result back. |
| `RAISE n`    | Pop the top value, add `n`, and push the result back. |
| `BET n`      | Push the integer `n` directly onto the stack. |
| `CALL`       | Duplicate the top value. Pops it, then pushes it back twice. |
| `FOLD`       | Subtraction. Pops `A` (top), then pops `B` (second), and pushes `B - A`. |
| `SNAPCALL`   | Addition. Pops `A` (top), then pops `B` (second), and pushes `B + A`. |
| `SHOWDOWN`   | Compare the top and bottom of the stack. If stack has fewer than 2 values, pushes `0` (done). If top equals bottom, removes both and pushes `1` (match). If they differ, removes both and pushes `2` (mismatch). |
| `DEAL`       | Read one line of input. Pushes the ASCII code of the first character. If input is empty or exhausted, pushes `0`. |
| `SHOW`       | Pop the top value and print it as a character (using its ASCII code). |
| `STACK`      | Pop the top value and print it as an integer. |
| `CHECK`      | Peek at the top value and print it as an integer **without popping it**. Useful for debugging. |
| `ALLIN n`    | Conditional jump. Pops the top value — if it is `0`, jumps to line `n`. If it is not `0`, execution continues normally. Lines are **1-indexed**. |
| `BLUFF`      | Swap the top two values on the stack. |
| `CUT`        | Move the top of the stack to the bottom. Pops the top value and inserts it at the very bottom of the stack. |
| `SHUFFLE`    | Move the bottom of the stack to the top. Removes the bottom-most value and pushes it on top. |
| `BUST`       | End the program immediately. |

### Key Concepts

- **Pushing values with `BET`:** `BET n` pushes the integer `n` directly onto the stack. For example, `BET 72` pushes `72` (ASCII `H`). This is the primary way to introduce specific values.
- **Incrementing with `RAISE`:** `RAISE` pops the top value and adds 1. `RAISE n` adds `n` instead. Useful for adjusting values or arithmetic in loops.
- **Conditional jumps:** `ALLIN n` is the only form of control flow. It pops and checks the top value — jumping to line `n` only when the value is zero.
- **Unconditional jumps:** Push `0` with `ANTE`, then immediately `ALLIN n`. Since the top is guaranteed to be `0`, the jump always fires.
- **Stack rotation:** `CUT` and `SHUFFLE` let you access values buried in the stack without losing them. `CUT` sends the top to the bottom; `SHUFFLE` brings the bottom to the top.
- **Swapping:** `BLUFF` swaps the top two values. Simpler than `CUT`/`SHUFFLE` when you only need to reorder the top two elements.
- **Addition with `SNAPCALL`:** Pops the top two values and pushes their sum. The addition counterpart to `FOLD` (subtraction).
- **Comparing with `SHOWDOWN`:** Compares the top and bottom of the stack. Returns `0` if the stack is exhausted (fewer than 2 values), `1` if they match, or `2` if they differ. Useful for palindrome checking and similar symmetry tests.

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
4. **`ALLIN 1`** — Pop the other copy. If it is `0` (meaning input was exhausted), jump to line 1, which reads again and will get `0` again, eventually ending. If it is not `0`, execution continues past the end and the program finishes.

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
BET 48      Line 1  → push 48 (ASCII '0')
            Line 2  (blank)
DEAL        Line 3  → read the character to repeat
DEAL        Line 4  → read the count (as a digit like '5')
SHUFFLE     Line 5  → bring 48 from the bottom to the top
FOLD        Line 6  → subtract 48 from the count's ASCII code
            Line 7  (blank)
CALL        Line 8  → duplicate the counter
ALLIN 21    Line 9  → if counter is 0, jump past the end → stop
            Line 10 (blank)
ANTE        Line 11 → push 0
RAISE       Line 12 → 0 + 1 = 1
FOLD        Line 13 → subtract 1 from the counter (decrement)
            Line 14 (blank)
BLUFF       Line 15 → swap counter and character (char on top)
CALL        Line 16 → duplicate the character
SHOW        Line 17 → print the character
BLUFF       Line 18 → swap back (counter on top)
ANTE        Line 19 → push 0
ALLIN 7     Line 20 → unconditional jump back to the loop check
```

**How it works:**

The program pushes `48` with `BET 48` — the ASCII code of `'0'`. This is used to convert a digit character to its numeric value (e.g., `'5'` is ASCII `53`, and `53 - 48 = 5`).

It then reads two inputs: the character to repeat and the repetition count (a single digit). It subtracts `48` from the count's ASCII code to get the actual number.

The main loop duplicates the counter and checks if it's `0` (done). If not, it decrements the counter by `1`, uses `BLUFF` to swap the counter and character so the character is on top, duplicates and prints it, then swaps back and loops.

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
BET 72     → H
SHOW
BET 101    → e
SHOW
BET 108    → l
SHOW
BET 108    → l
SHOW
BET 111    → o
SHOW
BET 44     → ,
SHOW
BET 32     → (space)
SHOW
BET 119    → w
SHOW
BET 111    → o
SHOW
BET 114    → r
SHOW
BET 108    → l
SHOW
BET 100    → d
SHOW
BET 33     → !
SHOW
```

This program prints `Hello, world!` by pushing each character's ASCII code directly with `BET` and printing it with `SHOW`. Each pair of lines pushes a value and immediately prints it as a character.

**Example run:**

```
$ python poker.py examples/helloworld.nlh
Hello, world!