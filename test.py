
# problem 1==========================================

def minRemovals(s):
    if len(s) < 1 or len(s) > 100:
        return -1
    stack = []

    for char in s:
        if stack and ((char == 'C' and stack[-1] == 'D') or (char == 'D' and stack[-1] == 'C')):
            stack.pop()
        elif stack and ((char == 'B' and stack[-1] == 'A') or (char == 'A' and stack[-1] == 'B')):
            stack.pop()
        else:
            stack.append(char)

    return len(stack)


s1 = "ABFCACDB"
print(minRemovals(s1))  # Output: 2

s2 = "ACBBD"
print(minRemovals(s2))  # Output: 5


s3 = "ADBCDCBDCABDCD"  # Output: 6
print(minRemovals(s3))


# problem 2==========================================
def groupAnagrams(strs):
    if len(strs) < 1 or len(strs) > 10**4:
        return []
    anagram_dict = {}

    for word in strs:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagram_dict:
            anagram_dict[sorted_word].append(word)
        else:
            anagram_dict[sorted_word] = [word]

    return list(anagram_dict.values())


strs1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
# Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
print(groupAnagrams(strs1))

strs2 = [""]
print(groupAnagrams(strs2))  # Output: [[""]]

strs3 = ["a"]
print(groupAnagrams(strs3))  # Output: [["a"]]

strs4 = ["dog", "god", "live", "evil", "loop", "pood"]
# Output: [['dog', 'god'], ['live', 'evil'], ['loop'], ['pood']]
print(groupAnagrams(strs4))
