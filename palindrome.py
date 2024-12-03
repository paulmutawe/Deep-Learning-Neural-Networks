class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        # Explicit if statement to check palindrome condition
        if str(x) == str(x)[::-1]:
            return True
        else:
            return False

solution = Solution()

x = 121

# Call the method and print the result
print(solution.isPalindrome(x))  # Output: True