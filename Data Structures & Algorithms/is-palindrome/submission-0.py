class Solution:
    def isPalindrome(self, s: str) -> bool:
        clean = ''.join(ch.lower() for ch in s if ch.isalnum())

        left, right = 0, len(clean) - 1
        while left < right:
            if clean[left] != clean[right]:
                return False
            
            left += 1
            right -= 1
        
        return True