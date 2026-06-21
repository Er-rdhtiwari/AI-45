package main

import "fmt"

// Problem: First Non-Repeating Character

func FirstNonRepeatingCharacter(s string) string {
	frequency := make(map[rune]int)

	for _, char := range s {
		frequency[char]++ // count how many times each character appears
	}

	for _, char := range s {
		if frequency[char] == 1 { // first character with count 1 is the answer
			return string(char)
		}
	}

	return "" // no non-repeating character found
}

func main() {
	fmt.Println(FirstNonRepeatingCharacter("leetcode")) // l
	fmt.Println(FirstNonRepeatingCharacter("aabbcdd"))  // c
	fmt.Println(FirstNonRepeatingCharacter("aabb"))     // ""
}

/*
### 1. Final Go Solution

The clean Go solution is above.

### 2. Intuition

Count how many times each character appears.
Then scan the string again from left to right.
The first character with frequency 1 is the first non-repeating character.
If no such character exists, return an empty string.

### 3. Approach

- Build a frequency map for all characters.
- Loop through the string again in original order.
- Return the first character whose frequency is 1.
- Return "" if every character repeats.

### 4. Dry Run

Example: s = "aabbcdd"

After counting:
frequency = {a:2, b:2, c:1, d:2}

Second pass:
a -> 2, skip
b -> 2, skip
c -> 1, return "c"

### 5. Gotchas

Don't forget in interviews:

- Empty string should return "".
- If all characters repeat, return "".
- Preserve order by doing a second pass over the original string.
- Use rune if input may contain Unicode characters.
- Do not return the first key from the map; map order is not guaranteed.

### 6. Complexity

Time Complexity: O(n)
Space Complexity: O(k), where k is the number of unique characters.

### 7. Related Problems

- First Unique Character in a String - Easy - Hash Map / Frequency Count
- Valid Anagram - Easy - Hash Map / Frequency Count
- Longest Substring Without Repeating Characters - Medium - Sliding Window / Hash Set
*/
