class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        best = 1

        all_set = set(nums)
        for num in all_set:
            
            if (num - 1) in all_set:
                continue
            
            x = num + 1
            curr = 1
            while x in all_set:
                curr += 1
                x += 1
            
            best = max(best, curr)
        
        return best