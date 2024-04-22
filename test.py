phân tích toán học cho thuật toán k-means
https://pages.github.com/
https://railway.app/new
https://docs.netlify.com/
https://www.uhostfull.com/free-hosting.php

https://www.youtube.com/watch?v=j1IbfQrT2Cs

https://www.youtube.com/@codekaratetutorials/videos link youtube có vẻ hay ho về drupal
https://www.youtube.com/@templatemonster/playlists một trang web câm như hến chả hiểu từ đâu ra, có lẽ sẽ có ích
https://www.youtube.com/@buildamodule một lish chi tiến vl, nhưng cũng có thể thấy drupal nó lỗi thời vl thế nào
https://www.youtube.com/@buildamodule trang web có vẻ ko tín lắm khi các video tương đối ngắn và sơ sài, không có quá nhiều ứng dụng


chuẩn bị tất cả nhứng thứ sẽ làm trong thứ 6, từ nhỏ nhất, dơn giản nhất, giải trí nhất tới trọng đại nhất buộc phải làm
- liên hệ với linh hỏi thăm dự án data, có vẻ c ấy cũng chưa bắt đầu
- mở lại các dự án về thương mại điện tử? dù cho nó đã quá thừa kẻ muốn kiếm tiền?
- chắc chắn phải hoàn thành yêu cầu của thầy về đồ án rồi, các video sẽ rất hữu dụng
 - nào nào, dự án web đã bỏ ngỏ quá lâu rồi, tại sao giờ vẫn chưa thấy làm?
- ồ, chuẩn bị chủ đề tiếng anh gia đình để nói với zany nữa, hmmm
- một góc thư thái để đọc sách? hmmm...cần dậy sớm mới có không khí và nhiệt độ tuyệt vời
- rèn luyện khả năng tập trung...không được đa việc cùng lúc! đo mới là cách rèn tư duy tốt nhất!
rồi dell làm đc cái gì luôn...súc vật


https://nuhado.co/
https://ireviewsach.com/
admin_menu
admin_views
backup_migrate
bundle_copy
ckeditor
ctools
devel
entity
field_group
libraries
minio
pathauto
references
taxonomy_manager 
token
transliteration
views
views_bilk_operations
views_field_view
# problem 1==========================================


from collections import defaultdict


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
    anagram_groups = defaultdict(list)

    for word in strs:
        count = [0] * 26

        for ch in word:
            count[ord(ch) - ord('a')] += 1

        anagram_groups[tuple(count)].append(word)

    return list(anagram_groups.values())


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
