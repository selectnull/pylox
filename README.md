pylox
=====

pylox is Python implementation of Lox programming language which is a
demo language from [Crafting Interpreters](http://www.craftinginterpreters.com/)
book by [Bob Nystrom](https://github.com/munificent).

I'm doing this because:

1. I want to learn about language design and implementation
2. I don't want to just read the book or copy and paste the code from it
   and I want to do something else than C or Java
3. Python is my main language these days and I want to use something I'm
   most comfortable with
4. Maybe after Python version I decide to reimplement it (or make my
   own toy language) in Go. Or force myself to learn Rust which seems
   like a good idea.
5. Fun.

This is **work in progress**.

Requirements
------------

Python 3.6 for no particular reasons except f-strings are used in few
places. Other than that, it could easily be ported to even Python 2.7
(but I don't plan to).

Run it
------

    python3 -m pylox [script]

License
-------

MIT.
