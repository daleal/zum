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

**Zum** (German word roughly meaning "_to the_" or "_to_" depending on the context, pronounced `/tsʊm/`) is a tool that lets you describe a web API using a [TOML](https://toml.io/en/) file and then call that API using your command line. This means that **the days of writing custom scripts to help you interact and develop each of your APIs are over**. Just create a `zum.toml`, describe your API and forget about maintaining more code!

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

The `endpoints` key contains every endpoint that you want to be able to access from `zum`. Each endpoint should also have a `route` value, a `method` value and may include a `params` value and a `body` value. Let's see an example:

```toml
[endpoints.dada]
route = "/sample-endpoint"
method = "post"
```

Notice that the header of the section consists of `endpoints.{something}`. **That `{something}` will be the name of your endpoint**. That means that, on the example, to query the endpoint, all you need to do is to run:

```sh
zum dada
```

With the existing configuration, `zum` will make a `POST` HTTP request to `http://localhost:8000/sample-endpoint` 🎵. Just 5 lines on a TOML file!

The endpoint configuration will be discussed more on a [dedicated section](#endpoints).

### Endpoints

Up until now, the examples shown are **really** simple. Rarely does an API endpoint not include some parameters on the URL or some request body. The idea of `zum` is to keep everything extremely simple, so let's see how to use URL parameters and the request body.

#### Parameters

Imagine that you have an API with an endpoint `/entity/:id` that returns an entity with the id `:id`. You would probably like to be able to just `zum entity 3` to get the entity with `:id` corresponding to `3`. Well, that's **exactly** what `zum` does. Let's first define the endpoint:

```toml
[endpoints.my-entity]
route = "/entity/{id}"
method = "get"
params = ["id"]
```

This configuration tells `zum` that it should replace the route string `{id}` for whatever `id` it receives from the command line as an argument (the command for that configuration should be `zum my-entity 3`). That makes sense. But why is the `params` value an array? Well, let's imagine that you want to search for all the appearances of some string on the entity model. The API endpoint will probably receive a `?query=` parameter. So let's describe this new endpoint:

```toml
[endpoints.search]
route = "/entity/{id}?query={query}"
method = "get"
params = ["id", "query"]
```

Now, you can run something like:

```sh
zum search 3 mystring
```

This will search `"mystring"` on the entity with id `3`. **But order matters**. Let's imagine that to you, it makes more sense to write the query string first. Then, your definition should be:

```toml
[endpoints.search]
route = "/entity/{id}?query={query}"
method = "get"
params = ["query", "id"]
```

Now, you can run something like:

```sh
zum search mystring 3
```

The query will be exactly the same. **This means that the array tells `zum` in which order to interpret the CLI parameters**.

#### Headers

Just like the parameters, the headers get defined as an array:

```toml
[endpoints.restricted]
route = "/secret"
method = "get"
headers = ["Authorization"]
```

To run this endpoint, you just need to run:

```sh
zum restricted "Bearer super-secret-token"
```

> ⚠ **WARNING**: Notice that, for the first time, we surrounded something with quotes. The reason we did this is that, without the quotes, the console has no way of knowing if you want to pass a parameter with a space in the middle or if you want to pass multiple parameters, so it defaults to receiving the words as multiple parameters. To stop this from happening, you can surround the string in quotes, and now the whole string will be interpreted as only one parameter with the space in the middle of the string. This will be handy on future examples, so **keep it in mind**.

This will send a `GET` request to `http://localhost:8000/secret` with the following headers:

```json
{
    "Authorization": "Bearer super-secret-token"
}
```

#### Request body

Just like the parameters and headers, the request body gets defined as an array:

```toml
[endpoints.create-entity]
route = "/entity"
method = "post"
body = ["name", "city"]
```

To run this endpoint, you just need to run:

```sh
zum create-entity dani Santiago
```

This will send a `POST` request to `http://localhost:8000/entity` with the following request body:

```json
{
    "name": "dani",
    "city": "Santiago"
}
```

As always, order matters.

```toml
[endpoints.create-entity]
route = "/entity"
method = "post"
body = ["city", "name"]
```

Now, to get the same result as before, you should run:

```sh
zum create-entity Santiago dani
```

**But what about types?** On the examples above, all the request body parameters are being sent **as strings**. Of course, you can cast the values to some types. The supported types are:

- `string`
- `integer`
- `float`
- `boolean` (`true` or `false`)
- `null`

To declare a type, let's imagine you have an API endpoint that receives two numbers `number1` and `number2` and adds them together. To describe this endpoint, you can use the following description:

```toml
[endpoints.add]
route = "/add"
method = "post"
body = [
    { name = "number1", type = "integer" },
    { name = "number2", type = "integer" }
]
```

Now, when you run

```sh
zum add 5 8
```

The request body will be:

```json
{
    "number1": 5,
    "number2": 8
}
```

Keep in mind that you can _mix and match_ the definitions. You can even define the parameter with the object notation and not include its type. You could define, for example:

```toml
[endpoints.example]
route = "/example"
method = "post"
body = [
    "parameter1",
    { name = "parameter2", type = "boolean" },
    { name = "parameter3" }
]
```

Now, `parameter1` will be sent as a string, `parameter2` will be casted as a boolean and `parameter3` will be sent as a string.

#### What about using all of the above?

Of course, sometimes you need to use parameters, headers **and** request bodies. For example, if you wanted to create a nested entity, you would need to use the parent's id as a parameter, the authorization headers and the new entity data as a request body. Let's describe this situation!

```toml
[endpoints.create-nested]
route = "/entity/{id}"
method = "post"
params = ["id"]
headers = ["Authorization"]
body = ["name", "city"]
```

Now, you can call the endpoint using:

```sh
zum create-nested 35 "Bearer super-secret-token" dani Santiago
```

This will call `POST /entity/35` with the following headers:

```json
{
    "Authorization": "Bearer super-secret-token"
}
```

And the following request body:

```json
{
    "name": "dani",
    "city": "Santiago"
}
```

As you can probably tell, `zum` receives the `params` first on the CLI, then the `headers` and then the `body`. In _pythonic_ terms, what `zum` does is kind of _unpacks_ the three arrays consecutively, something like the following:

```py
arguments = [*params, *headers, *body]
zum(arguments)
```

## `zum.toml` example

Here's a simple `zum.toml` file example:

```toml
[metadata]
server = "http://localhost:8000"

# zum my-entity 57
[endpoints.my-entity]
route = "/entity/{id}"
method = "get"
params = ["id"]

# zum search 57 mystring
[endpoints.search]
route = "/entity/{id}?query={query}"
method = "get"
params = ["id", "query"]

# zum create-entity "Bearer super-secret-token" dani Santiago
[endpoints.create-entity]
route = "/entity"
method = "post"
headers = ["Authorization"]
body = ["name", "city"]

# zum create-entity 35 "Bearer super-secret-token" dani Santiago
[endpoints.create-nested]
route = "/entity/{id}"
method = "post"
params = ["id"]
headers = ["Authorization"]
body = ["name", "city"]
```

With that config file (using a hypothetical existing API), you could `GET /entity/57` to get the entity with id `57`, `GET /entity/57?query=mystring` to search for the appearances of the word `mystring` on the model of the entity with id `57`, `POST /entity` with an authorization header and some request body to create a new entity and `POST /entity/35` with an authorization header and some request body to create a new nested entity, child of the entity with id `35`.

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
