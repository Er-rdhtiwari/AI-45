package main

import "fmt"

// 1. Final Go Solution
func ReverseString(s string) string {
	chars := []byte(s) // convert string to mutable bytes
	left, right := 0, len(chars)-1

	for left < right {
		chars[left], chars[right] = chars[right], chars[left] // swap ends
		left++                                                // move toward center
		right--
	}

	return string(chars)
}

func main() {
	fmt.Println(ReverseString("hello"))
}

/*
2. Intuition
- A string can be reversed by swapping characters from both ends.
- Use two pointers: one at the start and one at the end.
- After each swap, move both pointers toward the middle.
- Stop when the pointers meet or cross.

3. Approach
- Convert string to []byte because Go strings are immutable.
- Set left = 0 and right = len(s) - 1.
- Swap chars[left] and chars[right].
- Move left forward and right backward.
- Return the byte slice as a string.

4. Dry Run
Example: "hello"

chars = [h e l l o]
left=0, right=4 -> swap h and o -> [o e l l h]
left=1, right=3 -> swap e and l -> [o l l e h]
left=2, right=2 -> stop

Answer: "olleh"

5. Gotchas
Don't forget in interviews:
- Edge cases: empty string, single character string.
- Off-by-one errors: right should start at len(s) - 1.
- Pointer updates: increment left and decrement right after each swap.
- Base cases: loop should run while left < right.
- Unicode: []byte works for ASCII; use []rune if input may contain Unicode.

6. Complexity
- Time complexity: O(n)
- Space complexity: O(n), because strings are immutable and we create a byte slice.

7. Related Problems
- Reverse String, Easy, Two Pointers
- Valid Palindrome, Easy, Two Pointers
- Reverse Words in a String, Medium, Two Pointers / String Processing
*/
