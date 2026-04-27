class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_so_far = prices[0]
        best = 0

        for price in prices:
            profit = price - min_so_far
            if profit > 0:
                best = max(best, profit)

            min_so_far = min(price, min_so_far)

        return best