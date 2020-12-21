+++
title = "Modern C for C++ Peeps"
draft = false
+++

link
: <https://floooh.github.io/2019/09/27/modern-c-for-cpp-peeps.html>

tags
: [cpp]({{< relref "20201218231726-cpp" >}})

What you see in a lot of C code:

```c
typedef struct {
    int a, b, c;
} bla_t;

bla_t bla = ...;
```

But when you want to forwards declare such struct:

```c
// forward-declaring bla_t and a function using bla_t:
struct bla_t;
void func(struct bla_t bla);

// actual struct and function, using the typedef:
typedef struct {
    int a, b, c;
} bla_t;

void func(bla_t bla) { // <= warning 'parameter different from declaration'
    ...
}
```

That's why the **only** real way to declare struct in C is:

```c
typedef struct bla_t {
    int a, b, c;
} bla_t;
```