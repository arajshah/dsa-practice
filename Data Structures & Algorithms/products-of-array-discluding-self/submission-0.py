class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        left = [nums[0]]
        for i in range(1, len(nums)):
            left.append(left[i - 1] * nums[i])
        
        running = 1
        ans = [1] * len(nums)

        for i in range(len(nums) - 1, -1, -1):
            if i == 0:
                ans[i] = running
                continue

            ans[i] = left[i - 1] * running
            running = running * nums[i]
        
        return ans