print(open(__file__).read())
import unicodedata
code = unicodedata.normalize("NFKC", input("[AIS3 Jail] >>> "))
if (
    [code.count(c) for c in 'ais3'] == [1, 1, 1, 1] and
    set(code).isdisjoint('[]{}')
):
    print(eval(code, {'__builtins__': {}}, {}))
else:
    print('bad hacker') 
