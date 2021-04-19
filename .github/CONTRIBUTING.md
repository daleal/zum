### Before getting started

> **Thank you** for considering making a contribution to Zum. This tool is meant to help anyone and everyone, and **I love** that it can be improved by the very people that might some day use it. You really make this all possible! 💙

# How to contribute

Contributing is simple. First, consider the **scope** of what you would like to contribute. If you want to make a big change, **please [write an Issue](https://github.com/daleal/zum/issues/new) first**. Once the Issue has been discussed and you get assigned to that contribution, **fork this repository** and create a _feature_ branch from `master`. Make all your commits to this _feature_ branch on your fork. When the _feature_ is ready, you can make a Pull Request from your fork's _feature_ branch to this repository's `master` branch. **Please, make sure to write tests and to follow our coding conventions!** If instead of a big _feature_ you want to fix a small bug, or you want to add or fix some documentation, there's no need to write an Issue first. You can skip that step and continue with the next ones just described!

**Please be polite**. We are all doing this because we love it, and having a respectful community is **very** important to me.

If you want to talk to me directly, feel free to contact me using [Telegram](https://telegram.org/)! My handle is [@daaleal](https://t.me/daaleal). I would love to hear from you! Just remember to tell me that you come from this repository, so I can contextualize my thoughts!

## Getting started

All of Zum's _feature_ requests and documented bugs will live on its [Issues section](https://github.com/daleal/zum/issues). If you feel adventurous and want to write some lines of beautiful code, go and check it out! There's **always** something that can be improved, so don't be shy!

## Conventions

I don't have much conventions (other than those defined within [the linters](https://github.com/daleal/zum/actions/workflows/linters.yml)). There are only two things that I care about:

1. **I don't like in-code comments**. Of course, there are exceptions, but I find that they generally end up lying to the developers reading old code, so avoid them if you can.
2. **Optimize for readability**. I am all for efficient code, but if I have to trade readability for efficiency, unless the efficiency is vital to that piece of code, I wouldn't blink before writing readable code. Please, try to do the same when contributing to Zum!

Other things include following the linters, type annotating all your code (linters will enforce it, though) and writing tests. You can run each linter individually, with `make <linter>`. Some linters have automatic formatting, and that can be applied by running `make <linter>!` (_à la Ruby_). Our linters are `black`, `flake8`, `isort`, `mypy` and `pylint`. To run the tests, you can run `make tests`.
