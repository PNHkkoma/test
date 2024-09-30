
https://d-nb.info/1221936638/34
https://moscow.sci-hub.se/2326/b9cdc4a37bbb5cdfdaefcd9dd05d6166/wang2013.pdf#page=5&zoom=100,0,0

https://www.researchgate.net/profile/Salvador-Linares-Mustaros/publication/380395488_A_New_Methodological_Proposal_for_Classifying_Firms_According_to_the_Similarity_of_Their_Financial_Structures_Based_on_Combining_Compositional_Data_with_Fuzzy_Clustering/links/663a5d0e7091b94e93f9014d/A-New-Methodological-Proposal-for-Classifying-Firms-According-to-the-Similarity-of-Their-Financial-Structures-Based-on-Combining-Compositional-Data-with-Fuzzy-Clustering.pdf
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0268438

https://www.annualreviews.org/content/journals/10.1146/annurev-statistics-042720-124436 ||bản của thầy dễ dàng copy hơn
https://www.lyellcollection.org/doi/pdf/10.1144/gsl.sp.2006.264.01.01 || cái gì nhỉ...hmmm có vẻ cũng khá khó hiểu về lý thuyết
http://www.leg.ufpr.br/lib/exe/fetch.php/pessoais%3Aabtmartins%3Aa_concise_guide_to_compositional_data_analysis.pdf ||khá khó để lấy, lý thuyết cũng lan man
https://www.researchgate.net/publication/327387401_Compositional_Data_Analysis_in_Practice || hên xui lấy đc full text mà đọc
https://arxiv.org/pdf/2201.05197 || thử cái này đi
http://www.sediment.uni-goettingen.de/staff/tolosana/extra/CoDa.pdf || thử cái này xem

http://www.sediment.uni-goettingen.de/staff/tolosana/extra/CoDa.pdf
https://arxiv.org/pdf/2004.07881
https://arxiv.org/pdf/2201.02451
https://arxiv.org/pdf/2111.08953
https://www.annualreviews.org/content/journals/10.1146/annurev-statistics-042720-124436
https://d-nb.info/1221936638/34
https://is.muni.cz/do/rect/habilitace/1431/Hron/habilitace/7_Hron_et_al__2012_.pdf
https://www.york.ac.uk/media/economics/documents/hedg/workingpapers/2023/2316.pdf


trendyswagsnap@gmail.com
leonadoMacrus
hung12A52001

C:\Users\Administrator/.ssh/id_rsa
(C:\Users\dell/.ssh/id_rsa)
10.*;192.*;172.*;educationxr.vn;*.viettel.vn

https://www.youtube.com/watch?v=j1IbfQrT2Cs

https://www.youtube.com/@codekaratetutorials/videos link youtube có vẻ hay ho về drupal
https://www.youtube.com/@templatemonster/playlists một trang web câm như hến chả hiểu từ đâu ra, có lẽ sẽ có ích
https://www.youtube.com/@buildamodule một lish chi tiến vl, nhưng cũng có thể thấy drupal nó lỗi thời vl thế nào
https://www.youtube.com/@buildamodule trang web có vẻ ko tín lắm khi các video tương đối ngắn và sơ sài, không có quá nhiều ứng dụng




https://arxiv.org/search/?query=compositional+data&searchtype=all&source=header || trang web của đại học cornell 3



https://www.jstor.org/ ||web cung cấp cái gì đó, rảnh thì vô ko thì thôi



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
