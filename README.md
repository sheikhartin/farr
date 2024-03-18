## Farr

![GitHub repo status](https://img.shields.io/badge/status-active-green?style=flat)
![GitHub license](https://img.shields.io/github/license/sheikhartin/farr)
![GitHub contributors](https://img.shields.io/github/contributors/sheikhartin/farr)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sheikhartin/farr)
![GitHub repo size](https://img.shields.io/github/repo-size/sheikhartin/farr)

<img src="https://github.com/sheikhartin/farr/assets/64385550/28cdc310-faec-4a36-97f2-fd98bd292ee0" alt="Overcoming mental limitations" width="35%" height="35%" />

A programming language inspired by different things that aims to attract all kinds of developers. Ah, obviously that's impossible, but at least we have a good idea!

### Getting Started

In our programming language, the well-known Fizzbuzz program is as follows:

```zig
/**
 * A small challenge to label numbers into three categories...
 */

let rng_start = (
  readln!("Enter the starting point of the range: ")
  .toint()
);
let rng_end = (
  readln!("And also the end: ")
  .toint()
);
if rng_start >= rng_end = {
  println("The start value must be smaller than the end value!");
  exit!(1);
}

for let i in [rng_start..rng_end] = {
  if % i 15 == 0 = {
    println("...Fizzbuzz");
  } else if % i 3 == 0 = {
    println("...Fizz");
  } else if % i 5 == 0 = {
    println("...Buzz");
  } else = {
    println("${i}"); // Or just pass `i` as an argument!
  }
}
```

Yes, we use **prefix notation for mathematical operations** that clearly indicate priorities. You should also put an **equal sign behind the open brace before starting a block**...

Would you like to see more code samples from the Farr programming language? Go to the [examples](examples) folder...

### Usage

Clone it first:

```bash
git clone https://github.com/sheikhartin/farr.git \
&& cd farr
```

For both cool developers and adventurous users:

```bash
pip install -e . \
&& export FARRPATH=$PWD \
&& farr -h
```

However, virtualization is usually a better option:

```bash
docker build -t farr . \
&& docker run -it farr -h
```

Once Farr is installed, you can use it in several ways:

To run a `.farr` file, use the `run` command:

```bash
farr run examples/linear_search/sol02.farr
```

Remember to replace the example code with your own Farr code.

To start an interactive Farr shell (REPL), use the `shell` command:

```bash
farr shell
```

To swiftly execute Farr code snippets right from your command line, use the `cmd` command:

```bash
farr cmd 'println("Hello, world!");'
```

### Community

Join the Farr community [here](https://github.com/sheikhartin/farr/discussions) to discuss, ask questions, and share what you've built with Farr.

### License

This project is licensed under the MIT license found in the [LICENSE](LICENSE) file in the root directory of this repository.

### Disclaimer

As you know, you shouldn't use this language for a serious product \[at least not yet\]!
