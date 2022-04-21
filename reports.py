class Class2():
    def m(self):
        print("In Class2")


class Class3():
    def m(self):
        print("In Class3")


class Class4(Class2, Class3):
    pass


obj = Class4()
obj.m()

# Output:

# In Class2


######################################
######################################

# Why no Function Overloading in Python?
# Python does not support function overloading. When we define multiple functions with the same name, the later one always overrides the prior and thus, in the namespace, there will always be a single entry against each function name.

class A:
    def area(length,  breadth):
        return length * breadth

    def area(radius):
        return 3.14 * radius * radius

# We see what exists in Python namespaces by invoking functions locals() and globals(), which returns local and global namespace respectively.

# def area(radius):
#   return 3.14 * radius ** 2

# >>> locals()
# {
#   ...
#   'area': <function area at 0x10476a440>,
#   ...
# }
