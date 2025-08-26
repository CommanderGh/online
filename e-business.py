#instantiating or instantitation
#age = 75
#print("Introduction")

#input()
#name = input("What is your name?")
#age = input("What is your age: ")
##print("Hello", total)
#typecasting

#print("Data Structures")
#list, Tuples, Dictionary, Sets

#list are mutable
#fruits = ["orange","mango","pear"]

#Tuples are immutable
#fruits = ("orange","mango","pear")

#Dictionary hold key value pair kind of data
#fruits = {"001": "orange","002":"mango","003":"pear"}


#print("List Manipulations")

#list are mutable
#fruits = ["orange","mango","pear","watermelon"]
#fruits.append("kiwi")
#print("after append kiwi", fruits)

#fruits.remove("mango")
#print("after removing mango", fruits)

#fruits.pop(1)
#print("after popping the fruits at index 1", fruits)



#Dictionary hold key value pair kind of data
fruits = {"001": "orange","002":"mango","003":"pear"}
#update(), pop()
print("before adding kiwi", fruits)

fruits.update({"004": "kiwi"})
print("after updating kiwi", fruits)

fruits.pop("002")
print("after popping key 002", fruits)
