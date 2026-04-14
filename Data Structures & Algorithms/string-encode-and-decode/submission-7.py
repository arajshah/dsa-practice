class Solution:

    def encode(self, strs: List[str]) -> str:
        encoded_string = []
        for string in strs:
            encoded_string.append(str(len(string)))
            encoded_string.append('#')
            encoded_string.append(string)
        
        return "".join(encoded_string)
        
    def decode(self, s: str) -> List[str]:
        out = []

        i = 0
        while i < len(s):

            length = 0
            while s[i] != '#':
                length = length * 10 + int(s[i])
                i += 1
            
            out.append(s[i + 1: i + length + 1])
            i = i + length + 1
        
        return out
            