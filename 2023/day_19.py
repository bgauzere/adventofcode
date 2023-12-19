from utils import read_content
from dataclasses import dataclass

import logging

@dataclass(frozen=True)
class Range():
    x : tuple
    m : tuple
    a : tuple
    s : tuple  

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.m < other.m) or (self.x == other.x and self.m == other.m and self.a < other.a) or (self.x == other.x and self.m == other.m and self.a == other.a and self.s < other.s)

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
        
    def split(self, feature, threshold):
        if feature == "x":
            lr = (self.x[0],threshold)
            hr = (threshold+1,self.x[1])
            return (Range(lr,self.m,self.a,self.s), 
                    Range(hr,self.m,self.a,self.s))
        elif feature == "m":
            lr = (self.m[0],threshold)
            hr = (threshold+1,self.m[1])
            return (Range(self.x,lr,self.a,self.s), 
                    Range(self.x,hr,self.a,self.s))
        elif feature == "a":
            lr = (self.a[0],threshold)
            hr = (threshold+1,self.a[1])
            return (Range(self.x,self.m,lr,self.s), 
                    Range(self.x,self.m,hr,self.s))
        elif feature == "s":
            lr = (self.s[0],threshold)
            hr = (threshold+1,self.s[1])
            return (Range(self.x,self.m,self.a,lr), 
                    Range(self.x,self.m,self.a,hr))
        else:
            raise Exception("Invalid feature")
    
    def nb_items(self):
        nb_x = 1 +self.x[1] - self.x[0]
        nb_m = 1 +self.m[1] - self.m[0]
        nb_a = 1 +self.a[1] - self.a[0]
        nb_s = 1 +self.s[1] - self.s[0]
        return nb_x * nb_m * nb_a * nb_s
        

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
        is_greater = part[self.feature]>= self.threshold
        if self.greater == is_greater:
            return self.output
        else:
             return False 
    def decide_range(self,range):
        if self.threshold >= range[self.feature][0] and self.threshold <= range[self.feature][1]: # je suis concerné par le split
            # split
            
            if self.greater:
                r_low, r_high  = range.split(self.feature, self.threshold)
                return ((r_high,self.output),
                        (r_low, False))
            else:
                r_low, r_high  = range.split(self.feature, self.threshold-1)
                return ((r_high,False),
                        (r_low, self.output))
            
        elif range[self.feature][0] > self.threshold: # je suis dans la partie haute
            if self.greater:
                return ((range, self.output), None)
            else:
                return ((range, False), None)
        
        elif range[self.feature][1] < self.threshold: # je suis dans la partie basse
            if self.greater:
                return ((range, False), None)
            else:
                return ((range, self.output), None)
        else:
            raise Exception(f"Invalid range : {range = }, {self.feature = }, {self.threshold =}")
        
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
    
    def decide_range(self, range):
        cur_ranges = [range]
        ranges = []
        outputs = []

        for d in self.decisions:
            #print(cur_ranges)
            next_ranges = []
            for cur_range in cur_ranges:
                logging.info(f"{self.label} : {cur_range = }, {d.feature}, {d.threshold}")
                high, low = d.decide_range(cur_range)
                logging.info(f"{high = }, {low = }")
                range_h, output_h = high
                if output_h in ["A","R"]:
                    ranges.append(range_h)
                    outputs.append(output_h)
                elif output_h:
                    ranges.append(range_h)
                    outputs.append(output_h)
                else:
                    next_ranges.append(range_h)
                    

                if low is not None:
                    range_l, output_l = low
                    logging.info(f"{range_l = }, {output_l = }")
                    if output_l in ["A","R"]:
                        ranges.append(range_l)
                        outputs.append(output_l)
                    elif output_l: # on continue le prochaine decision
                        ranges.append(range_l)
                        outputs.append(output_l)
                    else:
                        next_ranges.append(range_l)
                        
            cur_ranges = next_ranges
        for range in cur_ranges:
            ranges.append(range)
            outputs.append(self.final)

        return ranges, outputs

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
    

    def process_range(self, range, decision_node_label):
        decision_node = self.decision_nodes[decision_node_label]
        ranges, outputs = decision_node.decide_range(range)
        accepted = []
        for range, output in zip(ranges, outputs):
            if output in ["A","R"]:
                if output == "A":
                    accepted.append(range)
            else:
                accepted =  accepted + self.process_range(range, output)
        return accepted    

    
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
        #print(parts[-1])
        i+=1
    return processor, parts

def first(content):
    processor, parts = parse_content(content)
    total = 0
    for p in parts:
        if processor.process(p) == "A":
            total += p.value()
    return total

def second(content):
    processor, parts = parse_content(content)
    range = Range((1,4000),(1,4000),(1,4000),(1,4000))
    #range = Range((1,1),(1,1),(1,1),(1,3))
    accepted = processor.process_range(range, "in")
    total = 0
    for r in sorted(accepted):
        logging.info(f"{r.nb_items()}")
    return sum([r.nb_items() for r in accepted])
if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format='LOG : %(message)s')

    content = read_content()
    print(f"res = {second(content)}")
    #print(Range((0,4000),(0,4000),(0,4000),(0,4000)).nb_items())