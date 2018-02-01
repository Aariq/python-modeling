phrase = input("Enter a phrase:")

phrase = phrase.replace(" ", "")

backwards = phrase[ : :-1]

if phrase ==  backwards:
    print("this is a palindrome")
else:
    print("this is not a palindrome")
