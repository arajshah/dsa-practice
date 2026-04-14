class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        out = []
        canon = defaultdict(list)

        for string in strs:
            freq_vector = [0] * 26
            for char in string:
                freq_vector[ord(char) - ord('a')] += 1

            canon[tuple(freq_vector)].append(string)

        return list(canon.values())