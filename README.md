<p align="center">
    <a href="https://github.com/daleal/zum">
        <img src="https://zum.daleal.dev/assets/images/zum-300x300.png">
    </a>
</p>

<h1 align="center">Zum</h1>

<p align="center">
    <em>
        Stop writing scripts to interact with your APIs. Call them as CLIs instead.
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

**Zum** (German word roughly meaning "_to the_" or "_to_" depending on the context, pronounced `/tsʊm/`) is a tool that lets you describe a web API using a [TOML](https://toml.io/en/) file and then interact with that API using your command line. This means that **the days of writing custom scripts to help you interact and develop each of your APIs are over**. Just create a `zum.toml`, describe your API and forget about maintaining more code!

## Installation

Install using pip!

```sh
pip install zum
```

## Why Zum?

While there are tools out there with goals similar to `zum`, the scopes are quite different. The common contenders are [OpenAPI](http://spec.openapis.org/oas/v3.0.3)-based tools (like [SwaggerUI](https://swagger.io/tools/swagger-ui/)) and [cURL](https://curl.se/). To me, using an OpenAPI-based documentation tool is essential on any large enough API, but the description method is **very** verbose and quite complex, so often times it is added once the API has quite a few endpoints. On the other hand, cURL gets very verbose and tedious very fast when querying APIs, so I don't like to use it when developing my APIs. As a comparison, here's a `curl` command to query a local endpoint with a JSON body:

```sh
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"name": "Dani", "city": "Santiago"}' \
    http://localhost:8000/living-beings
```

And here is the `zum` command to achieve the same result:

```sh
zum create application/json Dani Santiago
```

Now, imagine having to run this command hundreads of times during API development changing only the values on the request body, for example. You can see how using cURL is **not ideal**.

## Usage

### Basic Usage

The basic principle is simple:

1. Describe your API using a `zum.toml` file.
2. Use the `zum` CLI to interact with your API.

We get more _in-depth_ with how to structure the `zum.toml` file and how to use the `zum` CLI on [the complete documentation](https://zum.daleal.dev/docs/), but for now let's see a very basic example. Imagine that you are developing an API that gets the URL of [a song on YouTube](https://youtu.be/6xlsR1c8yh4). This API, for now, has only 1 endpoint: `GET /song` (clearly a [WIP](https://www.urbandictionary.com/define.php?term=Wip)). To describe your API, you would have to write a `zum.toml` file similar to this one:

```toml
[metadata]
server = "http://localhost:8000"

[endpoints.dada]
route = "/song"
method = "get"
```

Now, to get your song's URL, all you need to do is to run:

```sh
zum dada
```

Notice that, after the `zum` command, we passed an argument, that in this case was `dada`. This argument tells `zum` that it should interact with the endpoint described on the `dada` endpoint section, denoted by the header `[endpoints.dada]`. As a rule, to access an endpoint described by the header `[endpoints.{my-endpoint-name}]`, you will call the `zum` command with the `{my-endpoint-name}` argument:

```sh
zum {my-endpoint-name}
```

## Developing

Clone the repository:

```sh
git clone https://github.com/daleal/zum.git

cd zum
```

Recreate environment:

```sh
make get-poetry
make build-env
```

Run the linters:

```sh
make black flake8 isort mypy pylint
```

Run the tests:

```sh
make tests
```

## Resources

- [Issue Tracker](https://github.com/daleal/zum/issues/)
