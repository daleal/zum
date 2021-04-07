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

The [complete documentation](https://zum.daleal.dev/docs/) is available on the [official website](https://zum.daleal.dev/).

## Installation

Install using pip!

```sh
pip install zum
```

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

### `params`, `headers` and `body`

**Beware!** There are some nuances on these attribute definitions, so reading [the complete documentation](https://zum.daleal.dev/docs/) is **highly recommended**.

#### The `params` of an endpoint

On the previous example, the `route` was static, which means that `zum` will **always** query the same route. For some things, this might not be the best of ideas (for example, for querying entities on REST APIs), and you might want to interpolate a value on the `route` string. Let's say that there's a collection of songs, and you wanted to get the song with `id` _57_. Your endpoint definition should look like the following:

```toml
[endpoints.get-song]
route = "/songs/{id}"
method = "get"
params = ["id"]
```

As you can see, the element inside `params` matches the element inside the brackets on the `route`. This means that whatever parameter you pass to the `zum` CLI, it will be replaced on the `route` _on-demand_:

```sh
zum get-song 57
```

Now, `zum` will send a `GET` HTTP request to `http://localhost:8000/songs/57`. Pretty cool!

#### The `headers` of an endpoint

The `headers` are defined **exactly** the same as the `params`. Let's see a small example to illustrate how to use them. Imagine that you have an API that requires [JWT](https://jwt.io/introduction) authorization to `GET` the songs of its catalog. Let's define that endpoint:

```toml
[endpoints.get-authorized-catalog]
route = "/catalog"
method = "get"
headers = ["Authorization"]
```

Now, to acquire the catalog, we would need to run:

```sh
zum get-authorized-catalog "Bearer super-secret-token"
```

> ⚠ **Warning**: Notice that, for the first time, we surrounded something with quotes on the CLI. The reason we did this is that, without the quotes, the console has no way of knowing if you want to pass a parameter with a space in the middle or if you want to pass multiple parameters, so it defaults to receiving the words as multiple parameters. To stop this from happening, you can surround the string in quotes, and now the whole string will be interpreted as only one parameter with the space in the middle of the string. This will be handy on future examples, so **keep it in mind**.

This will send a `GET` request to `http://localhost:8000/catalog` with the following headers:

```json
{
    "Authorization": "Bearer super-secret-token"
}
```

And now you have your authorization-protected music catalog!

#### The `body` of an endpoint

Just like `params` and `headers`, the `body` (the body of the request) gets defined as an array:

```toml
[endpoints.create-living-being]
route = "/living-beings"
method = "post"
body = ["name", "city"]
```

To run this endpoint, you just need to run:

```sh
zum create-living-being Dani Santiago
```

This will send a `POST` request to `http://localhost:8000/living-beings` with the following request body:

```json
{
    "name": "Dani",
    "city": "Santiago"
}
```

**Notice that you can also cast the parameters to different types**. You can read more about this on the complete documentation's section about [the request body](https://zum.daleal.dev/docs/config-file.html#the-body-of-an-endpoint).

#### Combining `params`, `headers` and `body`

Of course, sometimes you need to use some `params`, some `headers` **and** a `body`. For example, if you wanted to create a song inside an authorization-protected album (a _nested entity_), you would need to use the album's id as a `param`, the "Authorization" key inside the `headers` to get the authorization and the new song's data as the `body`. For this example, the song has a `name` (which is a string) and a `duration` in seconds (which is an integer). Let's describe this situation!

```toml
[endpoints.create-song]
route = "/albums/{id}/songs"
method = "post"
params = ["id"]
headers = ["Authorization"]
body = [
    "name",
    { name = "duration", type = "integer" }
]
```

Now, you can call the endpoint using:

```sh
zum create-song 8 "Bearer super-secret-token" "Con Altura" 161
```

This will call `POST /albums/8/songs` with the following headers:

```json
{
    "Authorization": "Bearer super-secret-token"
}
```

And the following request body:

```json
{
    "name": "Con Altura",
    "duration": 161
}
```

As you can probably tell, `zum` receives the `params` first on the CLI, then the `headers` and then the `body`. In _pythonic_ terms, what `zum` does is that it kind of _unpacks_ the three arrays consecutively, something like the following:

```py
arguments = [*params, *headers, *body]
zum(arguments)
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

- [Official Website](https://zum.daleal.dev/)
- [Issue Tracker](https://github.com/daleal/zum/issues/)
- [Contributing Guidelines](.github/CONTRIBUTING.md)
