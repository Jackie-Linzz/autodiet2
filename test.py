__author__ = 'jerry'


class Person:

    def __init__(self):
        print 'init'

    @staticmethod
    def sayhello(hello):
        if not hello:
            hello = 'hello'
        print 'i will sya %s' % hello
    @classmethod
    def introduce(cls, hello):
        cls.sayhello(hello)
        print 'from hello method', cls

    def hello(self, hello):
        self.sayhello(hello)
        print 'from hello method', self

Person.sayhello('haha')
Person.introduce('hello world')

print '-'*40

p = Person()
p.sayhello('haha')
p.introduce('hello world')
p.hello('self.hello')