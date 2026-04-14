class Solution:

    def encode(self, strs: List[str]) -> str:
        encoded_string = ""
        for string in strs:
            encoded_string = encoded_string + str(len(string)) + '#' + string
        
        return encoded_string
        
    def decode(self, s: str) -> List[str]:
        print(s)
        out = []

        i = 0
        while i < len(s):

            j = 0
            while s[i] != '#':
                j = j * 10 + int(s[i])
                i += 1
            
            out.append(s[i + 1: i + j + 1])
            i = i + j + 1
        
        return out
            
