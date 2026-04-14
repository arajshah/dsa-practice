class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        heap = []
        canon = collections.Counter(nums)

        for num, freq in canon.items():
            heapq.heappush(heap, (freq, num))

            if len(heap) > k:
                heapq.heappop(heap)
            
        out = []
        for _ in range(k):
            out.append(heapq.heappop(heap)[1])

        return out

