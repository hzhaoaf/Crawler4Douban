class A:
	def __init__(self):
		print 'init a'
	def a(self):
		print 'a() in A'
	def a2(self):
		print 'a2() in A'

class B(A):
	def __init__(self):
		A.__init__(self)
	def a(self):
		print 'a() in B'


a = A()
b = B()

b.a()
b.a2()