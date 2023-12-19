from utils import read_content
from dataclasses import dataclass

@dataclass(frozen=True)
class Part():
    x : int
    m : int
    a : int
    s : int

    def __getitem__(self, feature:str):
        if feature == "x":
            return self.x
        elif feature == "m":
            return self.m
        elif feature == "a":
            return self.a
        elif feature == "s":
            return self.s
        else:
            raise Exception("Invalid feature")    

    def value(self):
        return self.x + self.m + self.a + self.s

class Decision():
    def __init__(self, feature, threshold,output, greater = True):
        self.feature = feature
        self.threshold = threshold
        self.output= output
        self.greater = greater

    def decide(self, part:Part):
        is_greater = part[self.feature]>=self.threshold
        if self.greater == is_greater:
            return self.output
        else:
             return False 
        
class DecisionNode():
    def __init__(self, label, decisions,final):
        self.label = label
        self.decisions = decisions
        self.final = final

    def decide(self, part:Part):
        for d in self.decisions:
            output = d.decide(part)
            if output : 
                return output
        return self.final
            
class Processor():
    def __init__(self, decision_nodes):
        self.decision_nodes = {}
        for n in decision_nodes:
            self.decision_nodes[n.label] = n
        self.input = self.decision_nodes["in"]
    def process(self, part:Part):
        decision = None
        decision_node = self.input 
        while decision is None:
            output = decision_node.decide(part)
            if output in ["A","R"]:
                decision = output
            else:
                decision_node = self.decision_nodes[output]
        return decision
    
def parse_content(content):
    i=0
    decision_nodes = []
    while content[i] != "":
        ## on parse les noeuds
        
        label,remaining = content[i].split("{")
        decisions_to_parse = remaining.split(",")
        final = decisions_to_parse[-1].split("}")[0]
        decisions = []
        for d in decisions_to_parse[:-1]:
            feature_threshold, output = d.split(":")
            if "<"  in feature_threshold:
                greater = False
                feature, threshold = feature_threshold.split("<")
            else:
                greater = True
                feature, threshold = feature_threshold.split(">")
            decisions.append(Decision(feature, int(threshold), output,greater))
        decision_node = DecisionNode(label, decisions, final)
        decision_nodes.append(decision_node)  
        i+=1 
    processor = Processor(decision_nodes)
    i+=1
    ## on parse les parts
    parts = []
    while i < len(content):
        part_str = content[i][1:-1]
        features = {}
        for feat in part_str.split(","):
            x, value = feat.split("=")
            features[x] = int(value)
        parts.append(Part(**features))
        print(parts[-1])
        i+=1
    return processor, parts

def first(content):
    processor, parts = parse_content(content)
    total = 0
    for p in parts:
        if processor.process(p) == "A":
            total += p.value()
    return total

if __name__ == "__main__":
    content = read_content()
    print(first(content))