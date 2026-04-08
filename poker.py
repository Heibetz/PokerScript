import sys
import os

lines = []
try:
   fileName = sys.argv[1]
   file = open(fileName)
   lines = file.read().split("\n")
   file.close()
except Exception as e:
   print(f"Error while opening file:\n{e}")
   sys.exit(0)

lyricsPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kennyrogers.txt")
try:
   with open(lyricsPath) as f:
      lyrics = f.read()
except Exception as e:
   print(f"Error loading lyrics file:\n{e}")
   sys.exit(0)

stack = []
pc = 0

def err(str):
   print("\n" + str + f" at line {pc}")
   sys.exit(0)

def pop(index = -1):
   if len(stack) < 1:
      err("Error: Stack underflow")
   return stack.pop(index)

while pc >= 0 and pc < len(lines):
   parts = lines[pc].split(" ")
   instr = parts[0]
   if instr == "ANTE":
      stack.append(0)
   elif instr == "RAISE":
      a = pop()
      stack.append(a+1)
   elif instr == "BET":
      if len(parts) < 2:
         err("Error: Expected instruction argument for BET")
      try:
         index = int(parts[1])
         if index < 0 or index >= len(lyrics):
            err("Error: BET index out of range")
         stack.append(ord(lyrics[index]))
      except ValueError:
         err("Error: Invalid argument for BET")
   elif instr == "CALL":
      a = pop()
      stack.append(a)
      stack.append(a)
   elif instr == "SHOW":
      print(chr(pop()), end="", flush=True)
   elif instr == "STACK":
      print(int(pop()), end="", flush=True)
   elif instr == "FOLD":
      a = pop()
      b = pop()
      stack.append(b - a)
   elif instr == "ALLIN":
      a = pop()
      if len(parts) < 2:
         err("Error: Expected instruction argument for ALLIN")
      try:
         line = int(parts[1]) - 1 # - 1 because list indexes start at 0
         if a == 0:
            pc = line - 1 # - 1 again because we're incrementing pc each instruction
      except:
         err("Error: Invalid instruction argument for ALLIN")
   elif instr == "CUT":
      a = pop()
      stack.insert(0, a)
   elif instr == "SHUFFLE":
      a = pop(0)
      stack.append(a)
   elif instr == "DEAL":
      try:
         stack.append(ord(input("")[0]))   
      except (IndexError, EOFError):
         stack.append(0)
   elif instr == 'BUST':
      break
   pc += 1

print('')