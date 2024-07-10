[![PyPI](https://github.com/voxelstack/icanc/actions/workflows/publish-to-pypi.yml/badge.svg)](https://pypi.org/project/icanc/)

# icanc
> Everything is so clear now.  
> I can C!  
> I can fight!

Learning data structures and algorithms **should** be done in C. Leetcode is a good way to practice and showcase coding skills, but I have never been thrilled about being constrained to a single source file.

`icanc` is a C preprocessor for bundling includes into a single source file you can submit to online judges. It also includes quality of life commands for generating source files and testing solutions.

## See it in action
https://github.com/voxelstack/icanc/assets/87827018/70e1ba31-66c9-4126-8a54-a9a946ecf740

[My leetcode repository](https://github.com/voxelstack/leet) is powered by `icanc`.

## Getting started
### Installation
`icanc` is available as a [pip package](https://pypi.org/project/icanc/):
```bash
pipx install icanc
```

### Create a new project
`icanc` creates a leetcode repository for you. Commands must be ran from inside the project root.

```bash
# Follow the prompts to create a project.
icanc init
```

### Try it out
Your new project comes with a solution and testcases for [beecrowd/1000](https://judge.beecrowd.com/en/problems/view/1000).

Take a look at `problems/beecrowd/1000/solution.c` and `problems/beecrowd/1000/testcases.toml`, and then check if the solution is correct:
```bash
# Test the default solution.c using testcases.toml
icanc test beecrowd 1000
```

The test should pass, which means we are ready to submit:
```bash
# Generate the submission for the default solution.c.
icanc submit beecrowd 1000 -c
```

The `-c` from the previous command copied the resulting submission to the clipboard, so you can go paste it on [beecrowd/1000](https://judge.beecrowd.com/en/problems/view/1000) and submit.

### world.execute(me)
That's the gist of it!

To solve [another problem](https://judge.beecrowd.com/en/problems/view/1001), scaffold a new solution:
```bash
# Create a solution and testcases for beecrowd/1001
icanc scaffold beecrowd 1000
```

### Watching for changes
You can run the test command in watch mode. While running, it will watch for changes to the `include/` directory and to the current problem's directory, rerunning all tests whenever a file changes.

```bash
# Test the default solution.c using testcases.toml
# Rerun on change.
icanc test beecrowd 1000 -w
```

### Multiple solutions
You may want to have multiple solutions for the same problem, either to practice different algorithms, optimize for different parameters, or showcase and compare alternate solutions.

To create a new solution for an existing problem, you can use the `--solution` option:

```bash
# Create a new solution for beecrowd/1000 called alt.c
icanc create solution beecrowd 1000 -s alt

# Test your new solution
icanc test beecrowd 1000 -s alt
```

### Multiple testcases
You may want to have multiple testcases for the same problem, either to organize your tests or to copy samples from something like [udebug](https://www.udebug.com/). When you test your solution, all testcases will be used.

To create new testcases for an existing problem, you can use the `--testcases` option:

```bash
# Create a new testcases file for beecrowd/1000 called alt.
icanc create testcases beecrowd 1000 -t alt

# Test your solution.
icanc test beecrowd 1000
```

## Project structure
```
leet/
├─ binaries/
├─ include/
│  └─ icanc.h
├─ problems/
│  └─ beecrowd/
│     └─ 1000/
│        ├─ solution.c
│        └─ testcases.toml
├─ submissions/
├─ templates/
│  ├─ solve_one.c
│  └─ solve_many.c
├─ icancrc.toml
├─ LICENSE
└─ README.md
```

### `leet/`
The `init` command will create a project folder with a name of your choice. All your code lives inside this folder, and this is where you should run commands from.

### `binaries/`
When solutions get compiled for testing, the resulting binaries will be placed on the `binaries/` folder. They are organized in subfolders by judge and problem.

`icanc` tests the compiled binaries automatically so you **should not** need to interact with this folder.

You **should not** commit this folder (the generated `.gitignore` already takes care of that).

### `include/`
This is where your header library will live. When compiling solutions the `include/` folder will be on your include path. Subfolders are supported, so you can organize your sources as you like.

To include files from your header library you **must** use a `#pragma icanc include` block.

### `problems/`
Your problem solutions live here, along with their testcases. They are organized in subfolders by judge and problem.

`icanc` generates these files for you, so you **should not** create files manually here.

 ### `submissions/`
When solutions get bundled for submitting, the resulting sources will be placed on the `submissions/` folder. They are organized in subfolders by judge and problem.

`icanc` can copy submissions to the clipboard automatically, so you **should not** need to interact with this folder.

You **should not** commit this folder (the generated `.gitignore` already takes care of that).

### `templates/`
When you create a new solution to a problem, it copies the source code from a given template. Those templates live in the `templates/` folder. You are free to manage your own templates, but keep in mind that `main.c` is the default and **should not** be removed.

### `icancrc.toml`
This file allows you to configure `icanc` for the current project.

## The preprocessor
When you generate a submission, all `icanc` imports will be resolved recursively and then copied over to your submission file, replacing the include directive. It works just like the [C preprocessor](https://gcc.gnu.org/onlinedocs/cpp/Include-Operation.html), meaning it's equivalent to copying the header file into each source file that needs it.

Of course, all restrictions from normal header files still apply. For example, you cannot include two header files that define a symbol witht he same name.
The preprocessor respects the `#pragma once` directive and will not include a file twice (if the file contains the directive).

With `icanc`, you can create a header library inside the `include/` directory and include headers normally on your leetcode solution! No more messy solutions with all the code dumped into a single file.

### #pragma icanc include
Including files from the `include/` directory **must** be done inside a `#pragma icanc include` block. Includes inside that block will be preprocessed recursively, and the include directives will be removed from the final submission. If you include a file from the `include/` directory outside a `#pragma icanc include` block, it will not be preprocessed and your submission will give you a compilation error.

Headers that are normally available on online judges **must** be included outside the `#pragma icanc include` block.

#### Example usage
```c
// include/icanc.h

#include <stdio.h>

void say()
{
    printf("Hello from icanc.h");
}
```

```c
// include/greeter.h

/*
 * icanc.h is from our header library,
 * it must be included inside a #pragma icanc include block.
 * 
 * You may add multiple include directives inside the same block.
 */
#pragma icanc include
#include <icanc.h>
#pragma icanc end

void greet()
{
    // Use a function from the included header.
    say();
}
```

```c
// problems/judge/problem/solution.c

#include <stdio.h>

#pragma icanc include
#include <greeter.h>
#pragma icanc end

int main()
{
    greet();
    return 0;
}
```

## Commands
For information on how to use each command, run the command with `--help`.

### `ci`
Test everything with machine friendly output and exit codes.

### `create`
Create solutions or testcases.

### `init`
Initialize an icanc project.

### `scaffold`
Create a solution and testcase files.

### `submit`
Bundle solution into a single source file for submission.

### `test`
Test a solution against given testcases.
