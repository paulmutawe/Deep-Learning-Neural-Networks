class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []    

        bracket_map = {')': '(', '}': '{', ']': '['}

        for char in s:

            if char in "({[":
                stack.append(char)
            elif char in ")}]":
                if not stack or stack.pop() != bracket_map[char]:
                    return False

        return not stack

x = "{[()]}"

solution = Solution()

print(solution.isValid(x))