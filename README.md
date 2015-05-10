#Prodo

A small imperative programming language for our CS 150 class. With a grammar inspired by staples like C and Python, Prodo aims to be a more readable and writable, yet strong-typed language by blending the features of imperative languages that we like the most.

## Features

Currently, Prodo only supports a very minimal set of features, mostly taken from C, Python, C++ and Ruby. These are the bare essentials for a language, including:
1. Primitive Data Types
    * int (Integer)
    * real (Floating Point)
    * bool (Boolean)
    * str (String)
    * array (List, Heterogeneous)
2. Declaration and assignment (strictly typed)
3. Function definition & calls
4. Conditional Control Structures
    * if
    * if-else
    * if-elseif-else
5. Iterative Control Structures
    * for-to-by (Counter-controlled)
    * while (Logic-controlled, pre-test)
    * loop-while (Logic-controlled, post-test)

## Grammar

The functional specification of Prodo's grammar and design is on [Google Drive](https://drive.google.com/open?id=1cG_ybEpNlpK-QZXljoqKl0M1LieyFlFE4Cx0WSL5368&authuser=0).

Keep in mind that Prodo is a class project. It's not meant to be used in production code, although the team _did_ strive to make it a good language. Some of the decisions in its design were also made to accomodate an easier implementation process and to further differentiate Prodo from existing languages.

## Compilation

Prodo's specs do not specify a method of implementation. In fact, it is (intentionally) vague as to the technical details of the language's intended implementation. This is because the specs are meant to be **functional** rather than **technical**. They only describe the design and grammar of Prodo, not how it is to be implemented.

The current and only implementation is dependent on [YAPPS](https://github.com/smurfix/yapps), a nice, lightweight Parser Generator written in Python. This satisfies one of the requirements of the class, which was that the compiler/interpreter be written in either Java or Python. Python was a natural choice because YAPPS was easy to use, and Python itself is fast and easy to write.

Currently, the YAPPS-generated parser takes Prodo code as input and outputs Python code. The Python code also accesses a pre-made Prodo Python module, which includes some built-in features.

There was also a previous, but (indefinitely) abandoned effort to create a Parser that outputs C++ code.
