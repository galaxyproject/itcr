# Fence client

## overview

Practical example to configure your server side application to retrieve the authenticated user's authorization record.

![image](https://user-images.githubusercontent.com/47808/54386078-6f00d200-4655-11e9-841b-62bcf804f7b9.png)


This document will illustrate:
a) how to configure revproxy (nginx) to recognize your application
b) how to call fence from within your application to retrieve authorization

It will not cover:
* How fence authenticates the user [see here for more](https://github.com/uc-cdis/fence#oidc--oauth2)
* How to configure authorization [see here for more](https://github.com/uc-cdis/compose-services#setting-up-users)


## setup

We assume you have installed either gen3's [docker-compose](https://github.com/uc-cdis/compose-services) or [cloud](https://github.com/uc-cdis/cloud-automation) services.

## your service

Add a stanza to your [compose-service](
https://github.com/uc-cdis/compose-services/blob/master/docker-compose.yml).

```
mock-workspace-service:
  build:
    context: ./mock-workspace
  container_name: mock-workspace-service
  networks:
    - devnet
  ports:
    - "5000:5000"
  depends_on:
    - fence-service
```

Then inform revproxy about your service

```
depends_on:
  - indexd-service
  - peregrine-service
  - sheepdog-service
  - fence-service
  - portal-service
  - pidgin-service
  # my service
  - mock-workspace-service
```


## revproxy

Next we need to tell `revproxy` about your service and what path it will respond to.

Add an nginx stanza to your [revproxy-service](
https://github.com/uc-cdis/compose-services/blob/master/docker-compose.yml).
See [this](https://github.com/uc-cdis/cloud-automation/blob/4241f40c6e10fd7096085a9456217b7b5e7cbb24/kube/services/revproxy/gen3.nginx.conf/fence-service.conf#L5) for inspiration.  
Note: the `/lw-workspace` path is maintained in `portal-service` and is not currently configurable.

```
#
location /lw-workspace/ {
  proxy_pass http://mock-workspace-service:5000/;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```


## query fence

Using a simple flask application, we respond to the request on /lw-workspace and simply return all relevant information to the caller.

The fence `/user` endpoint is documented [here](https://github.com/uc-cdis/fence/blob/master/openapis/swagger.yaml#L215) and the returned authorization payload is described [here](https://github.com/uc-cdis/fence/blob/master/openapis/swagger.yaml#L1805)



```
"""A mock API."""
from flask import Flask
from flask import jsonify
from flask import request
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """A simple way to create a Catch-All function which serves every URL including / is to chain two route filters. One for the root path '/' and one including a path placeholder for the rest.
       We can't just use one route filter including a path placeholder because each placeholder must at least catch one character."""

    # call fence and get information on the user
    fence_user = requests.get('http://fence-service/user', cookies=request.cookies)

    # just dump out all the data
    return jsonify(
        {'path': path,
         'headers': dict(**request.headers),
         'cookies': dict(**request.cookies),
         'fence': fence_user.json()
         })

if __name__ == '__main__':
    app.run(debug=True)
```
