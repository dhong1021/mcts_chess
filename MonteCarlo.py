import random
import math

class MonteCarlo:
    
    def __init__(self, root_node):
        self.root_node = root_node
        self.child_finder = None
        self.node_evaluator = lambda child, montecarlo: None
        
#     def child_finder(node):
#         for move in node.state.get_possible_moves():
#             child = Node(deepcopy(node.state))
#             child.state.move(move)
#             node.add_child(child)
    
#     def node_evaluator(self, node):
#         if node.state.won():
#             return 1
#         elif node.state.lost():
#             return -1
        
#     montecarlo.child_finder = child_finder
#     montecarlo.node_evaluator = node_evaluator
    
    def make_choice(self):
        best_children = []
        most_visits = float('-inf')  
        
        for child in self.root_node.children:
            if child.visits > most_visits:
                most_visits = child.visits
                best_children = [child]
            elif child.visits == most_visits:
                best_children.append(child)
                
        return random.choice(best_children) 
    
    def make_exploratory_choice(self):
        children_visits = map(lambda child: child.visits, self.root_node.children)
        children_visit_probabilities = [visit / self.root_node.visits for visit in children_visits]
        random_probability = random.uniform(0, 1)
        probabilities_already_counted = 0.
        
        for i, probability in enumerate(children_visit_probabilities):
            if probabilities_already_counted + probability >= random_probability:
                return self.root_node.children[i]
            
            probabilities_already_counted += probability
            
    def expand(self, node):
        self.child_finder(node, self)
        
        for child in node.children:
            child_win_value = self.node_evaluator(child, self)
            
            if child_win_value != None:
                child.update_win_value(child_win_value)
            
            if not child.is_scorable():
                self.random_rollout(child)
                child.children = []
                
        if len(node.children):
            node.expanded = True
            
    def simulate(self, expansion_count = 1):
        for i in range(expansion_count):
            current_node = self.root_node
            
            while current_node.expanded:
                current_node = current_node.get_preferred_child(self.root_node)
                
            self.expand(current_node)
            
    def random_rollout(self, node):
        self.child_finder(node, self)
        child = random.choice(node.children)
        node.children = []
        node.add_child(child)
        child_win_value = self.node_evaluator(child, self)
        
        if child_win_value != None:
            node.update_win_value(child_win_value)
        else:
            self.random_rollout(child)








