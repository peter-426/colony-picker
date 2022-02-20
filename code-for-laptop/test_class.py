#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello my name is " + self.name)
    
    def __self__(self):
        return "person:" + str(self.name) + ":" + str(self.age)

p1 = Person("John", 26)
p2 = Person("Paul", 36)

print('name=', p1.name, ',  age=', p1.age) 
p1.myfunc()
print(p1)

