# Contributing

I don't suppose that someone would want to use this so that there are only tips for me, how to deploy it.

Maybe later I would make a GitHub Actions Workflow for Auto Releases, but not now.

# Building & publishing the collection

- Get GALAXY_API_TOKEN from [here](https://galaxy.ansible.com/ui/token/)
- Build & publish the collection
  ```bash
  export GALAXY_API_TOKEN=token value here
  cd ansible-keepassxc-lookup
  ansible-galaxy collection build
  ansible-galaxy collection publish shameoff-keepassxccli-1.0.0.tar.gz --token $GALAXY_API_TOKEN
  ```
