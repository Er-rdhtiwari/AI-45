package main

import (
	"log/slog"
	"os"
)

// 1. Final Go Solution

func twoSum(nums []int, target int) []int {
	seenIndex := make(map[int]int, len(nums)) // value -> earlier index

	for index, num := range nums {
		need := target - num // number needed to complete target

		if prevIndex, found := seenIndex[need]; found {
			return []int{prevIndex, index} // earlier number + current number
		}

		seenIndex[num] = index // store only after checking to avoid same index
	}

	return []int{} // for variants where no answer is guaranteed
}

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))

	nums := []int{2, 7, 11, 15}
	target := 9

	logger.Info("two sum result", "indices", twoSum(nums, target))
}

/*
2. Intuition

For every number, ask: "Have I already seen the number that completes target?"
The needed number is target - current number.
A hash map lets us find that needed number in O(1) average time.
Store earlier numbers with their indices, because the answer asks for indices.

3. Approach

- Create a map: value -> index.
- Traverse nums from left to right.
- For each num, compute need = target - num.
- If need exists in the map, return its index and current index.
- Otherwise, store current num and index.

4. Dry Run

nums = [2, 7, 11, 15], target = 9

index = 0, num = 2, need = 7
seen = {}
store 2 -> 0

index = 1, num = 7, need = 2
seen has 2 -> 0
return [0, 1]

5. Gotchas

Don't forget in interviews:
- Edge cases: duplicates like [3, 3], target = 6.
- Return indices, not values.
- Check need before storing current num, or you may reuse the same element.
- With range, index is already correct; avoid manual off-by-one mistakes.
- Overflow is possible in real systems if target - num exceeds int bounds.

6. Complexity

Time complexity: O(n)
Space complexity: O(n)

7. Related Problems

1. Two Sum
   Difficulty: Easy
   Pattern: Hash map complement lookup

2. Two Sum II - Input Array Is Sorted
   Difficulty: Medium
   Pattern: Two pointers

3. 3Sum
   Difficulty: Medium
   Pattern: Sorting + fixed pointer + two pointers
*/
