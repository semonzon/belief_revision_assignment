import re

class BeliefSet():
    def __init__(self):
        self.beliefset = []  # Initialize an empty list to store beliefs
        
    def expansion(self, proposition, priority):
        # Method to add a proposition to the belief set at a specified priority
        if self.check(proposition):  # Check if the proposition is valid
            self.beliefset.insert(priority, proposition)  # Insert the proposition into the belief set
        
    def contraction(self, proposition):
        # Method to remove a proposition from the belief set
        self.beliefset.remove(proposition)  # Remove the proposition from the belief set

    def revision(self, proposition, priority):
        # Method to revise the belief set by replacing a proposition with another at a specified priority
        if self.check(proposition):
            self.beliefset.remove('¬' + proposition)  # Remove the negation of the proposition if present
            self.beliefset.insert(priority, proposition)  # Insert the proposition into the belief set
        
    def check(self, formula):
        # Method to check if a formula is valid
        pattern_proposition = r'^[a-z]$'  # Pattern for single propositional variables
        pattern_negation = r'^¬*[a-z]$'   # Pattern for negated propositional variables
        pattern_binary_operators = r'^(.) (->|v|\^|<->) (.)$'  # Pattern for binary logical operators
        pattern_with_parenthesis = r'^\((.)\) (->|v|\^|<->) \((.)\)$'  # Pattern for formulas with parentheses

        # Check if the formula matches any of the patterns
        if re.match(pattern_proposition, formula) or re.match(pattern_negation, formula):
            return True
        elif re.match(pattern_with_parenthesis, formula):
            match = re.match(pattern_with_parenthesis, formula)
            left_operand = match.group(1)
            operator = match.group(2)
            right_operand = match.group(3)
            return self.check(left_operand) and self.check(right_operand)
        elif re.match(pattern_binary_operators, formula):
            match = re.match(pattern_binary_operators, formula)
            left_operand = match.group(1)
            operator = match.group(2)
            right_operand = match.group(3)
            return self.check(left_operand) and self.check(right_operand)
        else:
            return False
        
    def empty(self):
        # Method to empty the belief set
        self.beliefset = []

    def printset(self):
        # Method to print the belief set
        print(self.beliefset)

    def check_add_formula(self, proposition):
        # Method to check and add a formula (not implemented)
        pass

    def simplify(self, proposition):
        # Method to simplify a formula (not fully implemented)
        pattern_with_parenthesis = r'^\((.)\) (->|v|\^|<->) \((.)\)$'
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

class Entailment():
    def __init__(self):
        pass

    def solve(self, beliefset, formula):
        beliefset_copy = beliefset.beliefset[:]  # Create a copy of the belief set
        if formula not in beliefset_copy:  # Check if formula is already in the belief set
            beliefset_copy.append(formula)  # Add the original formula to the belief set copy
        else:
            return True  # Formula is already in the belief set, so it trivially follows
        print("Belief set copy:", beliefset_copy)
        result = self.resolution(beliefset_copy)  # Call the resolution method
        print("Resolution result:", result)
        return result

    def resolution(self, beliefset):
        # Method to perform resolution-based inference to check for logical entailment
        clauses = self.to_clauses(beliefset)  # Convert belief set into clauses in CNF
        print("Initial Clauses:", clauses)
        new = set()  # Initialize an empty set to store new clauses
        
        while True:
            new_clauses = self.resolve(clauses)  # Resolve existing clauses to derive new ones
            print("New Clauses:", new_clauses)
            if not new_clauses:
                return False  # Conflict found, formula does not follow from beliefset
            if new_clauses.issubset(clauses):
                return True   # No new clauses produced, formula follows from beliefset
            new |= new_clauses  # Add new clauses to the set of clauses
            clauses |= new_clauses  # Update the set of clauses with new ones

    def to_clauses(self, beliefset):
        # Method to convert the belief set into clauses in Conjunctive Normal Form (CNF)
        clauses = set()  # Initialize an empty set to store clauses
        
        for belief in beliefset:
            if belief.startswith("¬"):  # If belief starts with negation
                clauses.add(frozenset([belief]))  # Add a singleton set with the negated belief
            else:
                clauses.add(frozenset([belief, "False"]))  # Add a set with belief and "False" (as negation)
        
        return clauses  # Return the set of clauses

    def resolve(self, clauses):
        new = set()  # Initialize an empty set to store new clauses
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 != clause2:  # Ensure different clauses are selected
                    resolvents = self.resolve_pair(clause1, clause2)  # Resolve pairs of clauses
                    if resolvents:
                        new |= resolvents  # Add new resolvents to the set of new clauses
        return new  # Return the set of new clauses

    def resolve_pair(self, clause1, clause2):
        resolvents = set()  # Initialize an empty set to store new resolvents
        
        for literal1 in clause1:
            for literal2 in clause2:
                if literal1.startswith("¬") != literal2.startswith("¬"):  # Check for complementary literals
                    if literal1[1:] == literal2[1:]:  # Check if literals have the same symbol
                        resolvents.add(frozenset(clause1.union(clause2) - {literal1, literal2}))  # Resolve literals
        return resolvents  # Return the set of new resolvents

# Your other classes and code remain unchanged

# Example usage:
beliefset = BeliefSet()
entailment = Entailment()
beliefset.expansion("p", 0)
beliefset.expansion("¬q", 1)

print("Belief set:", beliefset.beliefset)

# Test with different formulas
print(entailment.solve(beliefset, "q"))
print(entailment.solve(beliefset, "p")) 
