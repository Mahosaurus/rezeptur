# rezeptur
Rezept service

Steps to get it running in Azure:
- Provide Docker Registry (one time activity)
- Dockerfile must be at the root of the repo
- Set up App Service and let it do the linkage between repo and registry
- Grant App Service all permissions to push and pull from Docker Registry (non-essential)
- Add all necessary secrets into Configuration
    - E.g. ```DOCKER_REGISTRY_SERVER_USERNAME``` (happens automatically)
    - E.g. ```DOCKER_REGISTRY_SERVER_URL``` (happens automatically)
    - E.g. ```DOCKER_REGISTRY_SERVER_PASSWORD``` (happens automatically)
    - Port to be exposed is 8080, app.py exposes Port 8080 (check)
    - WEBSITES_PORT=8080 (set in configulation)
- In the deployment center: Select admin login for App Service (I think so at least) (non-essential)

```
git config --local --add core.sshCommand 'ssh -i ~/.ssh/X.rsa'
```
