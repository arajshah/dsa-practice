class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        canon = {}

        for idx, num in enumerate(nums):
            diff = target - num

            if diff in canon:
                return [canon[diff], idx]
            else:
                canon[num] = idx
        
        