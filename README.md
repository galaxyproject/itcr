# Year 1 ends Sept 30

## Usage scenario
1. Select datasets from Gen3 data browser (starting at portal or at Galaxy data source that redirects to browser)
2. Click on “Analyze data in Galaxy” button in data browser to launch/navigate to Galaxy
3. Galaxy starts and datasets + metadata from portal are added to history
4. User can run tools/workflows on data in place and outputs are placed in object storage bucket
5. Concrete example: run pathway activity tools on TCGA RNA-seq breast cancer cohort (~1000 datasets)

## Requirements
* Galaxy will run inside FISMA moderate environment
* Datasets will not be copied into Galaxy; only UUIDs will be copied into Galaxy

## Assumptions/Goals
* Single-tenant Galaxy instance
* Integration platform preferences: (1) Gen3; (2) ISB or FireCloud; (3) Cavatica; ideal: Gen3 running on cancer cloud(s) and orchestrating Galaxy provisioning/deployment


## Examples
* [gen3 aware workspace](docs/fence/README.md)
* [gcsfuse docker](docs/gcsfuse/README.md)
