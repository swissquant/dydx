# Python Template (with Poetry)

## Getting started

If you create this repository from the template, make sure to replace certain strings:

- `APPLICATION_NAME` in:

  - `pyproject.toml`
  - `helm/values.yml`
  - `.github/workflows/cicd-workflow.yml`

- `K8S_NAMESPACE` in:

  - `.github/workflows/cicd-workflow.yml`

- `APPLICATION_USER` in:
  - `Dockerfile`

## Build Docker image locally

Ultimately the CI will take care of building a suitable Docker image and push them to the registry. However if you want to test the image locally you can build it with the following command:

```bash
docker build -t my-application --ssh default .
```

Such command uses the `--ssh` option to allow the Docker Engine to forward SSH agent connections. In this way Docker can securely use the local SSH key to pull private GitHub repositories.

## Push new version

```
git tag 1.4.0 && git push --tags
```
