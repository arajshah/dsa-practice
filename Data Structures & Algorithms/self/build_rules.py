from collections import defaultdict

class BuildRules:

    def __init__(self, rules):
        self.graph = defaultdict(list)
        self.remaining = defaultdict(int)
        self.built = set()
        self.all_nodes = set()

        for dependent in rules:
            self.all_nodes.add(dependent)

            for dependency in rules[dependent]:

                self.graph[dependency].append(dependent)
                self.remaining[dependent] += 1
                self.all_nodes.add(dependency)
        
    def startBuild(self):
        '''
        Returns a list of files that can be built initially
        '''
        ans = list(node for node in self.all_nodes if self.remaining[node] == 0 and node not in self.built)
        
        return ans


    def buildTarget(self, target):
        '''
        Returns a list of files that can be built after target is built
        '''
        if not target in self.all_nodes:
            raise ValueError("Target file not found in graph")
        
        if target in self.built:
            raise ValueError("Target already built")
        
        if self.remaining[target] != 0:
            raise ValueError("Target has unresolved dependencies. Target cannot be built")

        self.built.add(target)
        ans = []

        for dependent in self.graph[target]:
            self.remaining[dependent] -= 1
            if self.remaining[dependent] == 0:
                ans.append(dependent)
            
        return ans

rules = {
    "foo.c": ["foo.d", "foo.e"],
    "foo.d": ["bar.a", "bar.b"],
    "foo.e": [],
    "bar.a": [],
    "bar.b": [],
}
br = BuildRules(rules)
print(br.startBuild())
print(br.buildTarget('bar.a'))
print(br.buildTarget('bar.b'))
print(br.buildTarget('foo.c'))


