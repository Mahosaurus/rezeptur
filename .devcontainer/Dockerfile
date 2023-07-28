# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.2/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
FROM mcr.microsoft.com/vscode/devcontainers/python:3.9@sha256:29ca94ddf0f254cb36e311ae59520c4dee33a35de7c0b2f1bd7b91650d368ee0

# Optionally: Add Zscaler cert to container (allows SSL)
COPY .devcontainer/Dockerfile .devcontainer/sgre_zscaler_cert* /etc/ssl/certs/
RUN cat /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/sgre_zscaler_cert > /etc/ssl/certs/ca-certificates.crt; exit 0
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
RUN update-ca-certificates

RUN pip install poetry
