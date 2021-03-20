<h1 align="center">Zum</h1>

<p align="center">
    <em>
        Stop writing scripts to test your APIs. Call them as CLIs instead.
    </em>
</p>

<p align="center">
<a href="https://pypi.org/project/zum" target="_blank">
    <img src="https://img.shields.io/pypi/v/zum?label=version&logo=python&logoColor=%23fff&color=306998" alt="PyPI - Version">
</a>

<a href="https://github.com/daleal/zum/actions?query=workflow%3Atests" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/daleal/zum/tests?label=tests&logo=python&logoColor=%23fff" alt="Tests">
</a>

<a href="https://codecov.io/gh/daleal/zum" target="_blank">
    <img src="https://img.shields.io/codecov/c/gh/daleal/zum?label=coverage&logo=codecov&logoColor=ffffff" alt="Coverage">
</a>

<a href="https://github.com/daleal/zum/actions?query=workflow%3Alinters" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/daleal/zum/linters?label=linters&logo=github" alt="Linters">
</a>
</p>

**Zum** (German word roughly meaning "_to the_" or "_to_" depending on the context, pronounced `/tsʊm/`) is a tool that lets you describe an API using a [TOML](https://toml.io/en/) file and then call that API using your command line. This means that **the days of writing custom scripts to help you develop each of your APIs are over**. Just create a `zum.toml`, describe your API and forget about maintaining more code!

## Installing

Install using pip!

```sh
pip install zum
```

## Usage

### The config file

The first thing that you need to do in order to use `zum` is to describe the API that you're trying to ping using a config file, named `zum.toml`. This TOML file should contain the following keys:

#### `metadata`

The `metadata` key contains everything that is not data about an endpoint of the API itself, but that is needed in order to query the API. This key should contain the following values:

- `server`: The base URL where the API is hosted.

As an example, the first lines of your `zum.toml` file for a development environment should probably look similar to this:

```toml
[metadata]
server = "http://localhost:8000"
```

This indicates to `zum` that the API endpoints are located at `http://localhost:8000`. Easy enough, right?

#### `endpoints`

The `endpoints` key contains every endpoint that you want to be able to use from `zum`. Each endpoint should also have a `route` value, a `method` value and may include a `params` value and a `body` value. Let's see an example:

```toml
[endpoints.endpointname]
route = "/endpoint-name"
method = "post"
```

Notice that the header of the section consists of `endpoints.{something}`. **That `{something}` will be the name of your endpoint**. That means that, on the example, to query the endpoint, all you need to do is to run:

```sh
zum endpointname
```

With the existing configuration, `zum` will make a `POST` HTTP request to `http://localhost:8000/endpoint-name`. Just 5 lines on a TOML file!

The endpoint configuration will be discussed more on a [dedicated section](#endpoints).
