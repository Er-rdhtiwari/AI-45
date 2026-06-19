package main

import "fmt"

// 1. Final Go Solution
func isAnagram(s string, t string) bool {
	if len(s) != len(t) {
		return false // anagrams must have the same length
	}

	charCount := make(map[rune]int)

	for _, char := range s {
		charCount[char]++ // count every character in s
	}

	for _, char := range t {
		charCount[char]-- // match every character from t
		if charCount[char] < 0 {
			return false // t has an extra or wrong character
		}
	}

	return true
}

func main() {
	fmt.Println(isAnagram("listen", "silent"))
}

/*
2. Intuition

Two strings are anagrams if they contain the same characters with the same frequency.
Count characters from the first string.
Subtract characters using the second string.
If any count goes below zero, the second string has a mismatch.

3. Approach

- If lengths are different, return false.
- Store character frequencies from s in a map.
- Traverse t and decrease each character count.
- If any count becomes negative, return false.
- Otherwise, return true.

4. Dry Run

Example: s = "anagram", t = "nagaram"

After counting s:
charCount = {a:3, n:1, g:1, r:1, m:1}

Process t:
n -> 0
a -> 2
g -> 0
a -> 1
r -> 0
a -> 0
m -> 0

No count is negative, so return true.

5. Gotchas

Don't forget in interviews:
- Edge cases: empty strings, different lengths, repeated characters.
- Off-by-one errors: loop through every character in both strings.
- Pointer updates: not relevant here.
- Base cases: length mismatch should return false immediately.
- Overflow/modulo issues: not relevant for this problem.

6. Complexity

Time Complexity: O(n)
Space Complexity: O(k), where k is the number of unique characters.

7. Related Problems

- Group Anagrams - Medium - Hash Map / Frequency Counting
- Valid Palindrome - Easy - Two Pointers
- Minimum Window Substring - Hard - Sliding Window / Hash Map
*/
