
# # make a class KB that can be used to store and manipulate knowledge bases.
# from copy import deepcopy
# from typing import Any

# from colorama import Fore
# import re

# # FACTS = [
# #     "M(x, y) => M(x-1, y) & M(x, y-1) & M(x+1, y) & M(x, y+1)",
# #     "P(x, y) => B(x-1, y) & B(x, y-1) & B(x+1, y) & B(x, y+1)",
# #     "W(x, y) => S(x-1, y) & S(x, y-1) & S(x+1, y) & S(x, y+1)",
# #     "M(x, y) => ~P(x, y) & ~W(x, y)",
# #     "P(x, y) => ~M(x, y)",
# #     "W(x, y) => ~M(x, y)",
# # ]

# # class KB:
# #     def __init__(self, facts):
# #         facts = deepcopy(facts)
# #         self.percept = []
# #         self.view = {}
        
# #     def add(self, facts, position):
# #         self.percept.extend(facts)
# #         self.addToView(facts, position)
        
# #     def addToView(self, facts, position):
# #         self.view[position] = facts
    
# #     def update(self):
        
        
# #     def print(self):
# #         # loop through the view and print the facts
# #         print(Fore.YELLOW + "Percept:" + Fore.WHITE)
# #         for position in self.view:
# #             print(self.view[position])
        
# # construct a FOLKB class that can be used to store and manipulate knowledge bases.

# class Literal:
#     def __init__(self, literal):
#         literal = literal.replace(" ", "")
#         if (literal[0] == "~"):
#             self.negated = True
#             literal = literal[1:]
#         else: 
#             self.negated = False
#         self.value = literal[0]
#         # use regex to get the x and y values
#         self.x = int(re.findall(r'\d+', literal)[0])
#         self.y = int(re.findall(r'\d+', literal)[1])
#         # print(self.x, self.y)
    
#     def display(self):
#         literal = self.value + "(" + str(self.x) + "," + str(self.y) + ")"
#         if not self.positive:
#             literal = '~' + literal
#         return literal
    
#     def __call__(self, postitive_state) -> Any:
#         # print(self.display())
#         if postitive_state:
#             self.positive = not self.negated
#         else:
#             self.positive = self.negated
#         return self.positive
# # class FOLKB:

# class Disjunction:
#     def __init__(self, disjunction):
#         self.literals = []
#         # use regex to get the literals
#         for literal in disjunction.split("|"):
#             self.literals.append(Literal(literal))
#     def display(self):
#         disjunction = ""
#         for literal in self.literals:
#             disjunction += literal.display() + " | "
#         return disjunction[:-1]
#     def __call__(self) -> Any:
#         # print(self.display())
#         temp = [i(True) for i in self.literals]
#         if True in temp:
#             self.positive = True
#         else:
#             self.positive = False
#         return self.positive
            
# class Proporsition:
#     def __init__(self, proporsition):
#         self.disjunctions = []
#         # use regex to get the disjunctions
#         for disjunction in proporsition.split("&"):
#             self.disjunctions.append(Disjunction(disjunction))
# # t = Literal("P(5, 7)")()
# t = Disjunction("~P(5, 7)|~W( 5, 7)|M(5, 7)")()
# print(t)
