class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left, right = 0, 0
        best = 0
        occurence_map = {}

        while right < len(s):

            if s[right] in occurence_map:
                prev_idx = occurence_map[s[right]]

                length = right - left
                best = max(best, length)
                
                if prev_idx >= left:
                    left = prev_idx + 1
            
            occurence_map[s[right]] = right
            right += 1
        
        best = max(best, right - left)
        return best
