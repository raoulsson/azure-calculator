# azure-calculator

Short Demo for Azure Functions - the app part, not the azure part...
Deployed is only "function_app.py"

Run: 

``` 
    source venv/bin/activate
    pip install -r requirements.txt 
```

or 

``` 
    source venv/bin/activate
    pip install azure.functions
```

Example calc: (58.5+2.2)*(3.8-1)

Once it's in Azure, call it like so via URL params, after URL encoding the calculation, over at e.g. https://www.urlencoder.org/:

via Curl & URL:

```
    curl -X GET "https://azure-calculator.azurewebsites.net/api/calc?calculation=%2858.5%2B2.2%29%2A%283.8-1"; echo
```

or the browser:

```
https://azure-calculator.azurewebsites.net/api/calc?calculation=%2858.5%2B2.2%29%2A%283.8-1
```


Or via Curl & POST:

```
    curl -X POST -H "Content-Type: application/json" -d '{"calculation":"(58.5+2.2)*(3.8-1)"}' https://azure-calculator.azurewebsites.net/api/calc; echo
```
