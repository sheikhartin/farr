### [1.4.2](https://github.com/sheikhartin/farr/releases/tag/1.4.2)

Moving the algorithms library to the [examples](examples) folder.

### [1.4.1](https://github.com/sheikhartin/farr/releases/tag/1.4.1)

A hotfix for interpreting arguments before creating a new environment!

### [1.4.0](https://github.com/sheikhartin/farr/releases/tag/1.4.0)

Enhancements and new features in invocation and operations:

- Added left (`<<`) and right (`>>`) shift operators for binary manipulation.
- Support for binary, octal, and hexadecimal literals.
- Enforced keyword-only arguments for optional parameters to prevent reassignment through positional arguments.
- Enhanced function, struct, and method invocation error handling with improved messages.

### [1.3.1](https://github.com/sheikhartin/farr/releases/tag/1.3.1)

Adding the `functools` module to our native libraries with these useful functions:

- `all`
- `any`
- `map`
- `partial`

### [1.3.0](https://github.com/sheikhartin/farr/releases/tag/1.3.0)

Smarter prefix and postfix operations; and a huge improvement in tests...

Because the use of terms has been reduced to two, now parentheses must be used to separate expressions! For a better understanding, look at the parse trees taken from the execution of code `^ 5 2 == 25;` in the previous version and then the current version:

```diff
- ModuleNode(body=[RelationalOperationNode(row=2,
-                                          column=7,
-                                          operator='EqualEqual',
-                                          left=ArithmeticOperationNode(row=2,
-                                                                       column=1,
-                                                                       operator='Power',
-                                                                       left=IntegerNode(row=2,
-                                                                                        column=3,
-                                                                                        value='5'),
-                                                                       right=IntegerNode(row=2,
+ ModuleNode(body=[ArithmeticOperationNode(row=2,
+                                          column=1,
+                                          operator='Power',
+                                          left=IntegerNode(row=2,
+                                                           column=3,
+                                                           value='5'),
+                                          right=RelationalOperationNode(row=2,
+                                                                        column=7,
+                                                                        operator='EqualEqual',
+                                                                        left=IntegerNode(row=2,
-                                                                                         value='2')),
-                                          right=IntegerNode(row=2,
-                                                            column=10,
-                                                            value='25'))])
+                                                                                         value='2'),
+                                                                        right=IntegerNode(row=2,
+                                                                                          column=10,
+                                                                                          value='25')))])
```

### [1.2.0](https://github.com/sheikhartin/farr/releases/tag/1.2.0)

Providing the ability to use all types of assignments even in chained form without any intermediate method...

### [1.1.0](https://github.com/sheikhartin/farr/releases/tag/1.1.0)

For better debugging, we will use a [linter](https://github.com/astral-sh/ruff).

### [1.0.1](https://github.com/sheikhartin/farr/releases/tag/1.0.1)

Fixing the dissimilarity of versions in different places...

### [1.0.0](https://github.com/sheikhartin/farr/releases/tag/1.0.0)

Introducing ternary expressions for inline conditional logic, a similar statement to switch, and prefix operations for direct arithmetic manipulation!

### [0.2.1](https://github.com/sheikhartin/farr/releases/tag/0.2.1)

Updating our `libs` folder structure...

```diff
  libs
  ├── algorithms
  │   ├── funda.farr
  │   └── searching.farr
  ├── database
  │   ├── funda.farr
  │   └── kime
  │       └── funda.farr
- ├── datetime
- │   └── funda.farr
+ ├── datetime.farr
- ├── fs
- │   └── funda.farr
+ ├── fs.farr
- ├── logging
- │   └── funda.farr
+ ├── logging.farr
  ├── math
  │   ├── funda.farr
  │   └── random.farr
- ├── os
- │   └── funda.farr
+ ├── os.farr
- └── platform
-     └── funda.farr
+ └── platform.farr
```

### [0.2.0](https://github.com/sheikhartin/farr/releases/tag/0.2.0)

An honest attempt to adapt to different platforms — there is still a possibility of error!

### [0.1.1](https://github.com/sheikhartin/farr/releases/tag/0.1.1)

Handling non-raw strings and their escape characters...

### [0.1.0](https://github.com/sheikhartin/farr/releases/tag/0.1.0)

The first release of Farr programming language! :relieved:
