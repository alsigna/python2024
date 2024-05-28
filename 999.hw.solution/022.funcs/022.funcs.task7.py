def foo(**kwargs):
    for var, value in kwargs.items():
        print(f"{var} = {value}")


foo(var1=32)
# var1 = 32

print("-" * 10)
foo(var1=32, var3="test")
# var1 = 32
# var3 = test
