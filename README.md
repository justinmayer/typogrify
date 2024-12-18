# Typogrify

[![GitHub Actions CI: continuous integration status](https://img.shields.io/github/actions/workflow/status/justinmayer/typogrify/main.yml?branch=main)](https://github.com/justinmayer/typogrify/actions)
[![PyPI Version](https://img.shields.io/pypi/v/typogrify)](https://pypi.org/project/typogrify/)
[![Downloads](https://img.shields.io/pypi/dm/typogrify)](https://pypi.org/project/typogrify/)

Typogrify provides a set of custom filters that automatically apply various transformations to plain text in order to yield typographically-improved HTML. While often used in conjunction with [Jinja][] and [Django][] template systems, the filters can be used in any environment.

[Jinja]: https://jinja.palletsprojects.com/
[Django]: https://www.djangoproject.com/

## Installation

The following command will install via `pip`. Pay particular attention
to the package name:

    python -m pip install typogrify

## Requirements

Python 3.9 and above is supported. The only dependency is [SmartyPants][], a Python port of a project by John Gruber.

[SmartyPants]: https://github.com/leohemsted/smartypants.py

Installing [Jinja][] or [Django][] is only required if you intend to use the optional template filters that are included for those frameworks.

## Usage

The filters can be used in any environment by importing them from
`typogrify.filters`:

    from typogrify.filters import typogrify
    content = typogrify(content)

For use with Django, you can add `typogrify` to the `INSTALLED_APPS` setting of any Django project in which you wish to use it, and then use `{% load typogrify_tags %}` in your templates to load the filters it provides.

Experimental support for Jinja is in `typogrify.templatetags.jinja_filters`.

## Included filters

### `amp`

Wraps ampersands in HTML with `<span class="amp">` so they can be styled with CSS. Ampersands are also normalized to `&amp;`. Requires ampersands to have whitespace or an `&nbsp;` on both sides. Will not change any ampersand which has already been wrapped in this fashion.

### `caps`

Wraps multiple capital letters in `<span class="caps">` so they can be styled with CSS.

### `initial_quotes`

Wraps initial quotes in `<span class="dquo">` for double quotes or `<span class="quo">` for single quotes. Works inside these block elements:

- `h1`, `h2`, `h3`, `h4`, `h5`, `h6`
- `p`
- `li`
- `dt`
- `dd`

Also accounts for potential opening inline elements: `a`, `em`, `strong`, `span`, `b`, `i`.

### `smartypants`

Applies [SmartyPants][].

### `typogrify`

Applies all of the following filters, in order:

- `amp`
- `widont`
- `smartypants`
- `caps`
- `initial_quotes`

### `widont`

Based on Shaun Inman’s PHP utility of the same name, replaces the space between the last two words in a string with `&nbsp;` to avoid a final line of text with only one word.

Works inside these block elements:

- `h1`, `h2`, `h3`, `h4`, `h5`, `h6`
- `p`
- `li`
- `dt`
- `dd`

Also accounts for potential closing inline elements: `a`, `em`, `strong`, `span`, `b`, `i`.

## Development

To set up your development environment, first clone the project. Ensure [`uv`][] is installed and then run:

    uv sync --all-groups
    uv run invoke setup

Each time you make changes to Typogrify, there are two things to do
regarding tests: check that the existing tests pass, and add tests for
any new features or bug fixes. You can run the tests via:

    uv run invoke tests

In addition to running the test suite, it is important to also ensure
that any lines you changed conform to code style guidelines. You can
check that via:

    uv run invoke lint

[`uv`]: https://docs.astral.sh/uv/
