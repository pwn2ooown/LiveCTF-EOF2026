# AIS3 Jail

- **Tags**: misc, pyjail
- **Author**: Vincent55

## Description

**It wouldn't be a true AIS3 competition without pyjail, isn't it?**

- Vincent55

## Hints

- `((G:=None.__new__.__self__.__getattribute__),(C:=G((),'%c%c%c%c%c%c%c%c%c'%(95,95,99,108,97,115,115,95,95))),(B:=G(C,'%c%c%c%c%c%c%c%c'%(95,95,98,97,115,101,95,95))))` 這串東西非常非常有用
- `a[123]` -> `a.pop(123)` and `dict['key']` -> `dict.get('key')` can bypass filter, 再來就是在這個題目的 python 版本找一個繼承 RCE Chain
