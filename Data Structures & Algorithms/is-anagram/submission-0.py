class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        def counter(string):
            canon = {}
            for char in string:
                if char in canon:
                    canon[char] += 1
                else:
                    canon[char] = 1
        
            return canon

        dict_s = counter(s)
        dict_t = counter(t)

        return dict_s == dict_t
        