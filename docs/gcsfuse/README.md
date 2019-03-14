# gcsfuse docker container

## overview

Practical example to configure a docker container to mount a google bucket into a filesystem.

![image](https://user-images.githubusercontent.com/47808/54389220-d4a48c80-465c-11e9-8596-9bb5400e10c6.png)


This document will illustrate:
a) how to configure gcsfuse within your docker container

It will not cover:
* How to create GCE VMs or buckets

## setup

We assume you have created and logged into your GCE VM and have access to a bucket.
`docker` should already be installed, if not there are many blog posts and documentation on how to accomplish this.


## your image

This example docker file:
* installs gcsfuse
* installs google's cloud utilities
* specifies that the user's `service_account.json` credentials should be mounted in the `/config` volume.
* launches a shell script to authenticate a start you service

```
FROM python:3.7.2

# creates a CLI environment:
# * python 3.7.2 environment
# * mounts gs://data.bmeg.io on /data.bmeg.io
# Uses service_account_email argument and config/service_account.json

ARG service_account_email

# install gcsfuse
RUN echo "deb http://packages.cloud.google.com/apt gcsfuse-jessie main" | tee /etc/apt/sources.list.d/gcsfuse.list; \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  apt-get update ; apt-get install -y apt-utils kmod && apt-get install -y gcsfuse

# install google utilities, ensure they are on path
RUN curl https://sdk.cloud.google.com | bash
ENV PATH=$PATH:/root/google-cloud-sdk/bin
RUN gcloud config set disable_usage_reporting true

# create a volume,  this image should be started with
VOLUME ["/config"]

# mount and sleep forever
COPY docker-start.sh /docker-start.sh
ENTRYPOINT ["/docker-start.sh"]
```

This example entrypoint authenticates to google, mounts the volume

You can specify the following environmental variables:

PROJECT=<the GCE project that contains the service account>
FUSE_PATH=<the directory to mount the bucket into>
BUCKET_NAME=<the bucket name>

Note:  the `--implicit-dirs` flag is necessary to parse object prefixes into directory names.

```
#!/usr/bin/env bash


# authenticate
gcloud auth activate-service-account \
  $service_account_email \
  --key-file=/config/service_account.json --project=$PROJECT

# create data dir
mkdir -p $FUSE_PATH

# mount the bucket.  
gcsfuse --implicit-dirs \
  --key-file=/config/service_account.json \
  $BUCKET_NAME  $FUSE_PATH

echo $FUSE_PATH mounted

# launch your service, for this example sleep forever
echo sleep infinity...
sleep infinity
```
