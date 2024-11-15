ect, the environment comparison tool, is the tool to compare your environments on files. If there is a difference in files, the differences will be logged in your console.

# How to run ect?
- First, you pip install the tool via this repository.
- Next, you write `ect --help` in your cli.
- You see from the documentation that there is a command called `run`
- When you use `ect run --help` in your cli, you see the arguments you need to give `ect run` to work.

## ect run arguments:
`--env-left` = name of environment folder you want to compare.
`--env-right` = name of other environment folder you want to compare.
`--name-dir` = name of folder that consists of all underlying files you want to compare.

## ect TOML config file:
ect works with a config file in which you can provide folders to include and folders to exclude in the search of the provided `--name-dir`.
If empty, ect will initialize an empty TOML config file. If the TOML config file exists, the information will be taken along.

The TOML config file should be called `ect_config.toml` and should consist of the following elements:
[ect]
include = []
exclude = []
