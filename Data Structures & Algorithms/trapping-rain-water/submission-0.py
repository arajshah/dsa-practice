class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max, right_max = 0, 0
        area = 0

        while left <= right:

            if left_max < right_max:

                if height[left] >= left_max:
                    left_max = height[left]
                    left += 1
                    continue
                
                area += min(left_max, right_max) - height[left]
                left += 1
            
            else:

                if height[right] >= right_max:
                    right_max = height[right]
                    right -= 1
                    continue
                
                area += min(left_max, right_max) - height[right]
                right -= 1
            
        return area
        