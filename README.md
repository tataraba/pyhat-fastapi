# PyHAT FastAPI

## Table of Contents

- [PyHAT FastAPI](#pyhat-fastapi)
  - [Table of Contents](#table-of-contents)
  - [About ](#about-)
  - [Getting Started ](#getting-started-)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
  - [The Basics ](#the-basics-)
    - [Getting Started](#getting-started)
    - [TailwindCSS](#tailwindcss)
    - [htmx](#htmx)
    - [Templates](#templates)
  - [The Story So Far](#the-story-so-far)
  - [What's Next?](#whats-next)
    - [Views](#views)
    - [Headers](#headers)
    - [Post Requests and CSRF Protection](#post-requests-and-csrf-protection)
    - [Partials/Fragments](#partialsfragments)
    - [Forms](#forms)
    - [Testing](#testing)
  - [Reproducibility](#reproducibility)
  - [What I've Learned](#what-ive-learned)

## About <a name = "about"></a>

This is an exploratory project to asses the workflow of a [PyHAT stack](https://github.com/PyHAT-stack/awesome-python-htmx) using FastAPI as the web framework. I'll be jotting down notes as I go.

## Getting Started <a name = "getting_started"></a>

This is meant to be exploratory, but if you feel like you want to try this out, feel free to clone/fork the repo and try things out for yourselves. Just keep in mind that this may be a moving target for now.

### Prerequisites

I'm using Python 3.11. I cannot guarantee that it would work with an earlier version.


### Installing

I use `pdm` as my package manager. If you use it as well, after cloning the project, you can just run the following command to get started:

```shell
pdm install
```

Otherwise, after cloning/forking to your local environment, make sure to create and activate a virtual environment

```shell
python -m venv .venv

# MacOS
source .venv/bin/activate

# Windows PS
.venv/Scripts/activate
```

Next, install the requirements:

```
python -m pip install -r requirements.txt
```


## The Basics <a name = "notes"></a>

These are notes I'll keep along the way as I build up the project. Will likely include reflections on how this might differ from other frameworks.

### Getting Started

It's easy to take for granted how easy/difficult it can be to get started with a project. For example, when I first tried Django, I was somewhat intimidated by the amount of "things" I had to know up front. This is likely trivial for individuals who already exist within the ecosystem.

A question I have here: Is it worth frontloading some of the complexity of getting a project started (i.e., Django) in opposition to getting started quickly with a microframework (i.e. FastAPI) and then having to worry about things like configuration, project structure, auth (if needed), templating system, etc...?

Some things of note:
-   Might be useful to use a package manager (I use `pdm`) to handle quickly setting up a project root with `pyproject.toml` and `venv` creating handle right away.
-   Would people want a cli command to quickly setup a predefined (best practices) project structure?
-   I don't mind creating a few empty `.py` files and folders as scaffolding, but maybe people don't prefer that flexibility?

Here would be my naive approach:
-   Use `pdm` to initiate a project
-   `pdm add fastapi, uvicorn[standard]
-   I like to create a README and other
-   Create the basic skeleton for project (At this point, might I want a cli command to do this for me? Not sure how I feel about this)
```
pyhat-fastapi/
┣ .venv/
┣ app/
┃ ┣ core/
┃ ┣ static/
┃ ┣ templates/
┃ ┣ views/
┃ ┣ main.py
┃ ┗ __init__.py
┣ tests/
┣ .gitignore
┣ pdm.lock
┣ pyproject.toml
┣ README.md
┗ requirements.txt
```
- Explanation:
  - `core` - contains config, custom exceptions, security, and any other "core" modules
  - `static` - images, css, fonts, js, etc...
  - `templates` - jinja templates/partials
  - `views` - naming it "views" to call out that these should work similar to Django function-based views
  - `tests` - because testing is cool 😎
  - `main.py` - where the FastAPI lives - should be thin (mostly settings)
  - Optional - `__main__.py` - can create an entry point for CLI if needed (would also require a module for cli functions)

I believe the skeleton above is thin enough to give the user flexibility, but structured enough to enable a PyHAT workflow.

The idea is that a user would spend most of their (front-end) time working within the `views` and `templates` directories, without having to muck around with CSS and JavaScript files.

Does this provide too much flexibility or not enough?

What's missing?

Notice that there is no database setup (yet).

The cool thing about PyStack is that it shouldn't matter what database you choose as your storage option. If you were using something like Django, you are benefitting from the built-in ORM and your options are limited.

Using a micro-framework allows you to be more discerning about what db solution you wish to use. This could include any ORM/ODM of your choice (SQLAlchemy, SQLModel, etc...).

Would users want database solution baked into a PyHAT solution? Or is it worth keeping options open (Postgres, MongoDB, EdgeDB, etc...)?

### TailwindCSS

Setting up Tailwind is fairly trivial using the `pytailwindcss` package.

The library is a wrapper to the [standalone Tailwind CLI](https://tailwindcss.com/blog/standalone-cli). Here are the limitations:
- Can't use other, external JS extensions/plugins/dependencies
- Can't use SCSS/PostCSS to overload directives

> As an aside:
>
> In one of the [PyHAT discussions](https://github.com/PyHAT-stack/awesome-python-htmx/discussions/2#discussioncomment-5740119), there was a question as to whether it would be worth building tooling to manage further parts of the "JS stack" to make up for these (and other) limitations.
>
> I think most people that might care for further JS tooling already have experience within the JS ecosystem.

Otherwise, it's time to add `pytailwindcss` to dependencies:

```shell
pdm add pytailwindcss

# using pip (make sure venv is active)
python -m pip install pytailwindcss
```

Running the `tailwindcss` command should download the binary and should show the help output for the `tailwindcss` command.

At this point, a user can choose to run the `tailwindcss init` (Tailwind CLI) which creates the default `tailwind.config.js` file.

You can also manually kick off other CLI commands (such as the build) with `--watch` or `--minify`

Although I did say that this is mostly non-trivial, it is a definite step that could be automated for a PyHAT type of application.

Lastly, running the build command (with a watcher) is a bit of boilerplate that would be nice to automate. It's an easy step to forget.

Elsewhere, I also included a subprocess command on app startup that ran the build command. This is especially useful to make sure your app has the most up-to-date css file.

### htmx

Setting up htmx is also straightforward. My question here is, should a "bundled" version of htmx be included in any PyHAT project, or should the user be prompted to download whichever new version?

For reference, `django-htmx` does not include htmx itself. It just provides the instructions of where to download it and how to include it in you template file. Per the project docs:

> django-htmx does not include htmx itself, since it can work with many different versions. It’s up to you to add htmx (and any extensions) to your project.

In contrast, the project `fuzzy-couscous` (CLI tool bootstraps a Django project with Tailwind/htmx support) has a specific command that downloads the latest htmx file. However, either way, you have to pass parameters for filename and directory.

Would that convenience be beneficial? (For reference, many of the htmx-related packages follow the _former_ route and merely add instructions, like what is written below.)

Otherwise, it's a matter of downloading the latest htmx file from its latest release.

[https://unpkg.com/browse/htmx.org/dist/](https://unpkg.com/browse/htmx.org/dist/)

I like to keep this in a `js` directory inside of my `static` folder.

Could create a CLI command to do this in an opinionated way...

The last step is to include the script file in the HTML, but I haven't mentioned the templates yet.

### Templates

The approach to templates may depend on use case.

I don't know if Jinja is the most popular templating language. It could be that the Django language is just as (if not more) popular by sheer number of people using Django. There are also other templating languages out there (i.e., [Cameleon](https://chameleon.readthedocs.io/en/latest/)).

But at this point, it seems relevant to be a little more opinionated than in other areas. This is because any tooling that interfaces with HTML (and htmx) will be intimately acquainted with the corresponding templating language. :blush:

But even with an opinionated choice (I know Jinja best, so let's go with that for now), there are still different approaches to how the templates themselves are structured.

My approach tends to look a little something like this:

```
templates/
┣ shared/
┃ ┣ base.html
┃ ┣ footer.html
┃ ┣ header.html
┃ ┣ scripts.html
┃ ┗ styles.htm
┣ error.html
┗ main.html
```

Explanation:
- `shared/base.html` - contains meta tags that will persist throughout site. I'll include variables for `<title>` and `<meta name="description">`. There are other meta type elements that could also include variables. For SEO purposes, it's good to vary these, so I send custom SEO data through with each Response. More on that later.
- `shared/scripts.html` - This contains the snippet to include htmx. (`<script src="/static/js/htmx.min.js"></script>`)
- `shared/styles.css` - This contains any stylesheets to be used throughout project. (`<link rel="stylesheet" href="/static/css/main.css" type="text/css" />`). While this will be the compiled TailwindCSS file, you could potentially add others if need be.
- `shared/header.html` - This ordinarly contains html relevant to site header and navigation. It's not always necessary to separate it out from `base.html` but I like to keep it separate for preference.
- `shared/footer.html` - Same as above. Only applies if you truly need it. I think having header/footer in separate files helps me find/edit these items pretty easily. Plus, they can be separated out from the `base.html` a lot easier in case you want to render a page without either of these items.
- `main.html` - This is where the primary "content" will be generated for each page view. With the help of htmx, most everything can live in here. However, without additional help (i.e., fragment rendering), we would likely need a `partials` directory that handles snippets of code to render for `htmx` calls.
- `error.html` - I guess pretty self-explanatory. I like to have custom error pages.
- From here, I would build separate templates as needed, but try to keep the number down as much as possible in order to maintain Locality of Behavior as much as possible.

For now, up to this point, I'm keeping the project pretty slim with few dependencies. But we'll go ahead and install Jinja2.

```shell
pdm add Jinja2

# using pip (make sure venv is active)
python -m pip install Jinja2
```

At this point, I wonder if a PyHAT would want/need to have a foundation of "shared" templates, which might include (at the very least) the `base.html` referenced above.

In which case, it would need to include a fair share of meta tags that are perhaps populated with defaults _or_ variables referenced in `pyproject.toml` _or_ perhaps populated from a CLI interface...

Either way, the goal would be to reduce a lot of the HTML boilerplate.

## The Story So Far

If I take a look at my `pyproject.toml` file (kindly generated by `pdm`), it looks something like this:

```toml
[tool.pdm]

[project]
name = ""
version = ""
description = ""
authors = [
    {name = "Mario Munoz", email = "pythonbynight@gmail.com"},
]
dependencies = [
    "fastapi>=0.95.1",
    "uvicorn[standard]>=0.22.0",
    "pytailwindcss>=0.1.4",
    "Jinja2>=3.1.2",
]
requires-python = ">=3.11"
license = {text = "MIT"}
```

It has occurred to me that while thinking of the PyHAT stack, I hadn't really considered a package manager (such as `pdm` or `poetry` or `hatch` or...) as a necessary part.

And indeed, it isn't.

But on the other hand, I'm starting to think that it _could_ be a good idea to incorporate a tool such as `pdm` in order to initiate a project like this. Part of the reason is that you could work off of the `dependencies` listed in the `pyproject.toml`&mdash;this would also allow for the definition of "dev only" dependencies (delineated in `pyproject.toml` as well), such as `pytest`, `ruff`, `black`, or other such tooling.

Hmm. Something to think about

## What's Next?

At this point, you can theoretically build a PyHAT application, but you would need to have some knowledge about the paradigms/patterns that go into it.

I've found [Django + htmx patterns](https://github.com/spookylukey/django-htmx-patterns) to be a pretty great resource. Much of the information applies even outside of the Django ecosystem.


### Views

The usage of Django function-based views (as opposed to Class Based Views) follows more closely what we would be accomplishing through the `views` directory.

Now, how closely do FastAPI routes emulate Django's function-based views?

I think I would need more experience with the latter to make a good determination.

In the meantime, here are a couple of items I would want to keep in mind for FastAPI "views."

1.  Views should remain thin. They should not be responsible for object mutations, updating data, or anything other than taking a request, performing some complex action, and returning an expected response without error. This allows for easier testing outside of the request context (the "complex action" can be tested independently).
```py
# Thin view example

@app.get("/do_a_thing")
async def do_something_cool(request: Request):
  thing = complex_action(request)
  return TemplateResponse(
    "cool.html",
    {
      "request": Request,
      "thing": thing,
    }
  )
```
2. Routes can be registered with FastAPI using the `APIRouter` object. However, ideally you wouldn't want to worry about registering routes with the FastAPI application. There are a couple of ways to do this dynamically (you can discover modules that use the `APIRouter` and load these automatically, but a package/tooling would need to be created for this).

### Headers

As of time of writing, there are [eight Request Headers](https://htmx.org/reference/#request_headers) that are (or can be) generated with each htmx request.

Accessing the values of these headers in FastAPI is just a matter of fetching it from the header dictionary:

```py
trigger = request.headers.get("HX-Trigger")
```

I noticed that the `asgi-htmx` package (similar to `django-htmx`) creates an `HtmxDetails` helper class that provides shortcuts to accessing htmx-specific headers.

I'm wondering if this is altogether necessary?

Presuming I didn't have the htmx documentation handy, I could inspect the Python object and find a list of properties (htmx request headers) that I have access to.

Hmmm. Maybe?

### Post Requests and CSRF Protection

Admittedly, this is a blind spot for me. In Django, CSRF protection is baked in, so you can just include the `csrf_token` in your tepmlate's `<form>` element, and that about handles it.

With htmx, you can include the token in a custom request header.

In this case, FastAPI does not have a solution out of the box for CSRF protection.

If your app requires CSRF protection, there are options with external libraries, such as `FastAPI JWT Auth` or `FastAPI CSRF Protect` or `csrf-starlette-fastapi`.

> **Note** You may not even really need CSRF protection due to how modern browsers handle SameSite cookies. There are [some edge cases](https://simonwillison.net/2021/Aug/3/samesite/) (detailed by Simon Willison) for which you'd still want to explicitly set up protection. But otherwise, you may be okay without it. See more at the [csrf-starlette-fastapi](https://github.com/gnat/csrf-starlette-fastapi) repo.
>

Another consideration with FastAPI is how routes are defined with the corresponding HTTP verb.

The short of it: FastAPI routes are typically decorated with the corresponding HTTP verb in the decorator:

```py
@app.get("/my_form")
async def my_form_get:
  # get stuff for full page load
  return TemplateResponse("simple_form.html", {"request": request})

@app.post("/my_form")
async def my_form_endpoint:
  # handle the POST request
  return RedirectResponse("/")
```

Now, you can accept both GET and POST requests for the same route, you would just need to use double decorators on the same route&mdash;though I would recommend the pattern above, as it is a little cleaner.

Note tha htmx POST requests would not need to follow the [POST/redirect/GET](https://en.wikipedia.org/wiki/Post/Redirect/Get) pattern, because an `hx-post` request does not return a full page anyway.

### Partials/Fragments

I would immediately lean toward using a package like `jinja2-fragments` to render partial content of a template.

This is perhaps the biggest quality of life improvement you could make with minimal effort, but it might take a bit of working with a codebase to really feel the difference this makes.

The TLDR version goes something like:
- With htmx, you will be rendering a lot of "partial" content into specific parts of the DOM
- This necessitates a lot of "small" files (or partials, if you will), corresponding to the specific htmx call
- A package like `jinja2-fragments` allows you to render a _fragment_ of an existing template, without the need for multiple smaller files
- You can read about this pattern over at htmx.org in an essay titled [Template Fragments](https://htmx.org/essays/template-fragments/)

For now, I'll keep it as a dependency. It seems like depending on an external package to enable this pattern is necessary as of now.

Ultimately, it would be great if Jinja2 enabled this pattern by default. It would need to provide a way to render a specific `{% block ... %}` of content without rendering the entire template.

The `jinja2-fragments` library (for FastAPI) does this by identifying a specified block (through an attribute such as `block_name`) and rendering only the content contained within.

Without out-of-the-box Jinja support, I think for now, even my "minimal" PyHAT FastAPI app would require this package

```shell
pdm add jinja2-fragments

# using pip (make sure venv is active)
python -m pip install jinja2-fragments
```

### Forms

Rendering forms in Django is, admittedly, pretty great because of the abstraction that allows you to define all input/validation in the same place.

Form handling with FastAPI is still pretty good, due to the type-hint system providing a certain level of validation.

However, this level of abstraction may make it a little less straightforward when adding styling/htmx attributes to each element of a form. In one sense, building forms "by hand" might actually be more useful.

But again, your mileage may vary depending on how much boilerplate you want to be writing in a larger web application.

With htmx, ensuring that the "submit" button of a form does a server call without leaving the page (and updating the form inplace) is fairly straightforward.

But providing inline validation as a user enters data in totally plausible.

I'll have to do some more experimentation to see how this might fit in within the PyHAT context.

### Testing

I want to flesh this out more. I think testing would be a lot more manageable if most of the route/view logic is kept segregated from the views.

But for more robust testing, I am thinking of [Playwright](https://playwright.dev/python/docs/intro), but I don't have much experience with it.

For an example of usage, couldn't go wrong with Andrew Knight's [Bulldoggy: The Reminders App](https://github.com/AutomationPanda/bulldoggy-reminders-app), where he builds a PyHAT-style app and uses `pytest` and `Playwright` for testing.

## Reproducibility

I mentioned elsewhere that using a package manager to leverage the use of `pyproject.toml` and (if available) a lock file might be beneficial, but seems like an odd requirement.

In that case, I would either add a pre-commit hook of some sort (if using a package manager) to export a regular, old requirements.txt file.

To do that with `pdm`, you would need to include this command:

```shell
pdm export -o requirements.txt
```

That creates a `requirements.txt` file that includes hashed versions for all dependencies/subdependencies.


## What I've Learned

There are plenty of places to introduce either existing tooling, or new interactions to help streamline a great PyHAT experience.

Many of the opportunities for creativity are out there to explore, and I may tackle one (or more) of these, but probably not until after I take [another look](https://github.com/PyHAT-stack/awesome-python-htmx) at the tools that are already out there.

If I wanted to outline the process to get to this point in the most "traditional" way possible, it would look something like this:

1.  Create project root directory
    1.  Use package manager to install dependencies in `pyproject.toml` or `requirements.txt`
    2.  Create directory structure outlined above
    3.  Choose database and corresponding ORM/ODM of choice and install those dependencies
2.  Download htmx and copy file in `static` directory
3.  Initiate `tailwindcss` in command line (which downloads/installs the binary)
4.  Create a template structure
    1.  Start with `base.html` that includes most of the meta tags
    2.  Include css and htmx script tags
    3.  Create `header.html` and `footer.html` as needed
5.  Create config file in the `core` directory to start delineating project/app configuration
6.  Start working on project logic

That's not all _too_ bad, but there is definitely room to improve this workflow.

In addition, there are several helpers that could be added to ease the htmx workflow in lieu of headers and fragments.