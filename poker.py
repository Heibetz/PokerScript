import sys

lines = []
try:
   fileName = sys.argv[1]
   file = open(fileName)
   lines = file.read().split("\n")
   file.close()
except Exception as e:
   print(f"Error while opening file:\n{e}")
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
      if len(parts) >= 2:
         try:
            stack.append(a + int(parts[1]))
         except ValueError:
            err("Error: Invalid argument for RAISE")
      else:
         stack.append(a + 1)
   elif instr == "BET":
      if len(parts) < 2:
         err("Error: Expected instruction argument for BET")
      try:
         stack.append(int(parts[1]))
      except ValueError:
         err("Error: Invalid argument for BET")
   elif instr == "CALL":
      a = pop()
      stack.append(a)
      stack.append(a)
   elif instr == "SNAPCALL":
      a = pop()
      b = pop()
      stack.append(b + a)
   elif instr == "SHOWDOWN":
      if len(stack) < 2:
         if len(stack) == 1:
            pop()
         stack.append(0)
      else:
         a = pop()
         b = pop(0)
         if a == b:
            stack.append(1)
         else:
            stack.append(2)
   elif instr == "SHOW":
      print(chr(pop()), end="", flush=True)
   elif instr == "STACK":
      print(int(pop()), end="", flush=True)
   elif instr == "CHECK":
      if len(stack) < 1:
         err("Error: Stack underflow")
      print(stack[-1], end="", flush=True)
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
   elif instr == "BLUFF":
      if len(stack) < 2:
         err("Error: BLUFF requires at least two values on the stack")
      a = pop()
      b = pop()
      stack.append(a)
      stack.append(b)
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