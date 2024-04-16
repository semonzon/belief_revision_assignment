# %%
import re

class BeliefSet():
    def _init_(self):
        self.beliefset = []
        
    
    def expansion(self, proposition, priority):
        if self.beliefset.check(proposition):
            self.beliefset.insert(priority, proposition)
        
    def contraction(self,proposition):
        self.beliefset.remove(proposition)

    def revision(self, proposition, priority):
        if self.beliefset.check(proposition):
            self.beliefset.remove('¬' + proposition)
            self.beliefset.insert(priority, proposition)

    def check(self,formula):
        # Define the regex patterns for the recursion
        pattern_proposition = r'^[a-z]$'
        pattern_negation = r'^¬*[a-z]$'
        pattern_binary_operators = r'^(.) (->|v|\^|<->) (.)$'
        pattern_with_parenthesis = r'^\((.)\) (->|v|\^|<->) \((.)\)$'


        # Check if the formula matches any of the patterns
        if re.match(pattern_proposition, formula) or re.match(pattern_negation, formula):
            return True
        elif re.match(pattern_with_parenthesis, formula):
            match = re.match(pattern_with_parenthesis, formula)
            left_operand = match.group(1)
            operator = match.group(2)
            right_operand = match.group(3)
            return self.check(left_operand) and self.check(right_operand)
        elif re.match(pattern_binary_operators,formula):
            match = re.match(pattern_binary_operators,formula)
            left_operand = match.group(1)
            operator = match.group(2)
            right_operand = match.group(3)
            return self.check(left_operand) and self.check(right_operand)
        else:
            return False
        

    # def check_symbol(self,symbol):
    #     symbols = ['->','¬','v','^','<->']
    #     open_par = ['(']
    #     close_par = [')']
    #     if symbol in symbols:
    #         return 'sym'
    #     elif symbol in open_par:
    #         return 'open_par'
    #     elif symbol in close_par:
    #         return 'close_par'
    #     return 'nothing'
    # def check_letter(self, proposition):
    #     if (len(proposition) == 1 and proposition.isalpha()) or (len(proposition) == 2 and proposition[0] == '¬' and proposition[1].isalpha()):
    #         return True
    #     return False
    
    def empty(self):
        self.beliefset = []

    def printset(self):
        print(self.beliefset)

    def check_add_formula(self, proposition):
        pass

    def simplify(self, proposition):
        pattern_with_parenthesis = r'^\((.)\) (->|v|\^|<->) \((.)\)$'   # ((p -> q) -> (p <-> r))
        pattern_morgan_1 = r'( ¬\( ) ((.)v(.) \) ) '
        pattern_morgan_2 = r'( ¬\( ) ((.)\^(.) \) ) '
        

        if re.match(pattern_with_parenthesis, proposition):
            match = re.match(pattern_with_parenthesis, proposition)
            left_operand = match.group(1)
            operator = match.group(2)
            right_operand = match.group(3)
            if operator == '<->':
                proposition == '(' + left_operand + '->' + right_operand + ')' + '^' + '(' + right_operand + '->' + left_operand + ')'
                return self.simplify(proposition)
            elif operator == '->':
                proposition ==  '¬' + left_operand + 'v' + right_operand 
                return self.simplify(proposition)
        elif re.match(pattern_morgan_1, proposition):
            match = re.match(pattern_morgan_1, proposition)
            left_operand = match.group(1)
            operator = match.group(2)
            right_operand = match.group(3)
            proposition = '¬' + left_operand + '^' + '¬' + right_operand
            return self.simplify(proposition)
        elif re.match(pattern_morgan_2, proposition):
            match = re.match(pattern_morgan_2, proposition)
            left_operand = match.group(1)
            operator = match.group(2)
            right_operand = match.group(3)
            proposition = '¬' + left_operand + 'v' + '¬' + right_operand
            return self.simplify(proposition)
        else:
            return proposition

    # beliefset = [p,q] -> ¬q,1 -> [p,¬q]
    # beliefset = [p,q] -> ¬q,2 -> [p,q] 
    


class Entailment(): #  method that checks whether a given formula logically follows from the belief base.
    def _init_(self): #beliefset = [p, q]. Is it formula= p v q correct?#beliefset = [p, q]. Is it formula= p v q correct?
        self.beliefset = BeliefSet()
        
    def solve(self, beliefset, formula):
        # Method to solve logical entailment: checks if 'formula' logically follows from 'beliefset'
        # Inputs:
        # beliefset: BeliefSet object representing the current set of beliefs
        # formula: string representing the formula to check for logical entailment
        # Returns:
        # True if 'formula' logically follows from 'beliefset', False otherwise
        beliefset_copy = beliefset.beliefset[:]
        beliefset_copy.append("¬(" + formula + ")")  # Add negation of the formula
        return self.resolution(beliefset_copy) 
    
    def resolution(self, beliefset):
        clauses = self.to_clauses(beliefset)
        new = set()
        while True:
            new_clauses = self.resolve(clauses)
            if not new_clauses:
                return False  # Conflict found, formula does not follow from beliefset
            if new_clauses.issubset(clauses):
                return True   # No new clauses produced, formula follows from beliefset
            new |= new_clauses # The set union operator, denoted by |= , is used to combine two sets into a new set containing all unique elements from both sets
            clauses |= new_clauses
    
    def to_clauses(self, beliefset):
        clauses = set()
        for belief in beliefset:
            if belief.startswith("¬"):
                clauses.add(frozenset([belief]))
            else:
                clauses.add(frozenset([belief, "False"]))
        return clauses
    
    def resolve(self, clauses):
        new = set()
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 != clause2:
                    resolvents = self.resolve_pair(clause1, clause2)
                    if resolvents:
                        new |= resolvents
        return new

    def resolve_pair(self, clause1, clause2):
        resolvents = set()
        for literal1 in clause1:
            for literal2 in clause2:
                if literal1.startswith("¬") != literal2.startswith("¬"):
                    if literal1[1:] == literal2[1:]:
                        resolvents.add(frozenset(clause1.union(clause2) - {literal1, literal2}))
        return resolvents

class Test():
    def _init_(self):
        pass
    def successpostulate(self):
        pass
    def inclusion(self):
        pass
    def vacuity(self):
        pass
    def consistency(self):
        pass
    def extensionality(self):
        pass

beliefset = BeliefSet() # FOR TESTING NOW
beliefset.expansion("p v q", 0)
beliefset.expansion("¬q", 1)
entailment = Entailment()
print(entailment.solve(beliefset, "p"))  # should output: True

# %%
bs = BeliefSet()

# %%
import re

def sigue_recursion(formula):
    # Define the regex patterns for the recursion
    pattern_proposition = r'^[a-z]$'
    pattern_negation = r'^¬*[a-z]$'
    pattern_binary_operators = r'^(.) (->|v|\^|<->) (.)$'
    pattern_extrange = r'^\((.)\) (->|v|\^|<->) \((.)\)$'


    # Check if the formula matches any of the patterns
    if re.match(pattern_proposition, formula) or re.match(pattern_negation, formula):
        # print('entra por a')
        return True
    elif re.match(pattern_extrange, formula):
        # If it's a binary operator, recursively check its operands
        match = re.match(pattern_extrange, formula)
        left_operand = match.group(1)
        operator = match.group(2)
        right_operand = match.group(3)
        # print('entra por 1 con left being:', left_operand, 'operator being:',operator,'and right being:',right_operand)
        return sigue_recursion(left_operand) and sigue_recursion(right_operand)
    elif re.match(pattern_binary_operators,formula):
        match = re.match(pattern_binary_operators,formula)
        left_operand = match.group(1)
        operator = match.group(2)
        right_operand = match.group(3)
        # print('entra por 2 con left being:', left_operand, 'operator being:',operator,'and right being:',right_operand)
        return sigue_recursion(left_operand) and sigue_recursion(right_operand)
    else:
        # print('falla en c')
        return False

# Ejemplos de uso
formulas = ['p', '¬p', 'p -> p', 'p ^ p', 'p v p', 'p <-> p', '(p -> p) ^ (p v p)', '(p -> p) -> (p v p)','q -> ¬¬r', '-> p']
# formulas = ['((p -> p) ^ (p v p))', '((p -> p) -> (p v p))']
for formula in formulas:
    print(f"La fórmula '{formula}' sigue la recursión especificada:", sigue_recursion(formula))


# %%


# %%