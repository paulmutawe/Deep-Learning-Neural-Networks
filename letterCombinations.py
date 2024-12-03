class Solution(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        if not digits:
            return []

        # Mapping of digits to corresponding letters
        digit_to_char = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }
        
        # Start with a list containing an empty string
        combinations = [""]
        
        for digit in digits:
            # Check if digit is valid
            if digit not in digit_to_char:
                continue  # Skip invalid digits
            
            # Fetch corresponding letters for the current digit
            possible_chars = digit_to_char[digit]
            
            # Create a temporary list to store new combinations
            new_combinations = []
            
            for prev in combinations:
                for char in possible_chars:
                    # Append the new character to the existing combination
                    new_combinations.append(prev + char)
            
            # Update combinations with the new list
            combinations = new_combinations
        
        return combinations

# Create an object of the Solution class
solution = Solution()

# Input string
x = "23"

# Call the function and print the result
output = solution.letterCombinations(x)
print(output)