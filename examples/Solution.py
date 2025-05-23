from euchre_bots import bots

class Solution():
    next_id = 0

    def __init__(self, features):
        self.features = features
        self.score = 0.0
        self.count = 0
        self.id = Solution.next_id
        Solution.next_id = Solution.next_id + 1

    def update_score(self, score, count):        
        sum = (self.score * self.count) + score
        self.count = self.count + count
        self.score = (sum + score) / self.count
    
    def __str__(self):
        return f"{self.id}, {self.features}, {self.score}"