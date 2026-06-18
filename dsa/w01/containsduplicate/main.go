package main

func containsDuplicate(nums []int) bool {
	seen := make(map[int]bool, len(nums)) // stores numbers already visited

	for _, num := range nums {
		if seen[num] { // duplicate found
			return true
		}

		seen[num] = true // mark current number as visited
	}

	return false // every number was unique
}

/*
1. Final Go Solution

func containsDuplicate(nums []int) bool {
	seen := make(map[int]bool, len(nums))

	for _, num := range nums {
		if seen[num] {
			return true
		}
		seen[num] = true
	}

	return false
}

2. Intuition

Use a hash set to remember numbers already seen.
If a number appears again, it is a duplicate.
Return immediately when the first duplicate is found.
If the loop ends, all numbers are unique.

3. Approach

- Create a map to act as a hash set.
- Traverse nums from left to right.
- If nums[i] is already in the map, return true.
- Otherwise, add it to the map.
- Return false after the loop.

4. Dry Run

nums = [1, 2, 3, 1]

seen = {}
num = 1 -> not found -> seen = {1}
num = 2 -> not found -> seen = {1, 2}
num = 3 -> not found -> seen = {1, 2, 3}
num = 1 -> found -> return true

5. Gotchas

Don't forget in interviews:
- Empty or one-element arrays return false.
- Check for duplicate before inserting the current number.
- Negative numbers and zero work normally as map keys.
- Avoid O(n^2) nested loops when nums can be large.
- No pointer updates, base cases, overflow, or modulo issues here.

6. Complexity

Time complexity: O(n)
Space complexity: O(n)

7. Related Problems

- Contains Duplicate II | Easy | Hash Set + Sliding Window
- Two Sum | Easy | Hash Map Lookup
- Contains Duplicate III | Hard | Bucket / Balanced Tree
*/
