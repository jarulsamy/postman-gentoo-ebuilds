# Postman Gentoo Ebuilds

> Disclaimer: This is a community driven project and it is not associated with
> Postman.

A generator for ebuild specs for all Postman versions.

# Motivation

I wanted to use Postman on Gentoo, but there was no ebuild to easily install it.
Instead of just installing it by hand as a one-off (like a sane person), I
decided to:

1. Learn how to write Gentoo ebuilds.
2. Scour the internet for the Postman download API URLs and schemas.
3. Write a generator to create ebuilds for not just the latest version, but any
   version of Postman ever released.

Why do something once when you can spend a few hours automating it?!

# Usage

Just run the script and look at your newly created ebuilds in `./dist`.

```cli
$ uv run generate-ebuilds.py
```

Propagate the files to the repository of your choice!

## Notes

- Postman is primarily installed under `/opt` with a wrapper to launch in
  `/usr/bin`.

- Paths for the icon is derived from the latest version, there is no guarantee
  it will work for older ones.

- Postman has a handy changelog endpoint that outputs versions and download
  links via JSON ([funnily enough, also inspired by a Gentoo
  user](https://github.com/postmanlabs/postman-app-support/issues/2967)).

  Have a look [https://dl.pstmn.io/changelog](https://dl.pstmn.io/changelog).
