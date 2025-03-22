# Ansible KeepassXC Lookup Plugin

This is an Ansible lookup plugin that fetches data from a KeePass database using `keepassxc-cli`.  
It allows you to retrieve credentials or custom properties from your KeePass database via the command line,  
making it especially useful in environments where a GUI is not available.

## Requirements

- Python 3.x
- Ansible, of course
- `keepassxc-cli` must be installed and available in your system PATH. (See below for details)
- Your KeePass database (.kdbx) file must be accessible.

## Installation

### KeePassXC 

See [KeePassXC site](https://keepassxc.org/) for details of Installation.  
In my case installing it via `apt install keepassxc` was enough. I'm sure, other package managers
also have this package

### The plugin itself

To be honest, I wouldn't like to post this like an ansible-galaxy collection by several reasons. ~~(first of them is lazyness)~~

So, I suggest you just copy the file `plugins/lookup/keepassxc-cli.py` to your `ansible_plugins` folder. 

If you want to store it near with your ansible-playbooks. Do next:

1. Create/Edit an `ansible.cfg` file and add in defaults section the string `lookup_plugins=./plugins/lookup`
  ```ini
  [defaults]
  lookup_plugins=./plugins/lookup
  ... # other params
  ```
2. Paste the file `plugins/lookup/keepassxc-cli.py` in `./plugins/lookup`

## Usage

### Before usage

- Set the following variables in your inventory or playbook:
  - `keepass_dbx`: Path to the KeePass database file.
  - `keepassxc_pwd`: Master password for the KeePass database.
  - Optionally, `keepass_key`: Path to the key file if used.

Or, alternatively, you can set environment variables:

- `ANSIBLE_KEEPASSXC_PWD` Password
- `ANSIBLE_KEEPASSXC_KEY_FILE` Path to keyfile

In your playbook, you can use the lookup plugin like this:

```yaml
- name: Retrieve password from KeePass
  debug:
    msg: "{{ lookup('keepass_cli', 'A_name_of_your_credentials_entity', 'password') }}"

- name: Retrieve a custom property from KeePass
  debug:
    msg: "{{ lookup('keepass_cli', 'Entry (can contain spaces)', 'custom_properties', 'my_prop_key') }}"
```

Ensure that the required variables are defined, for example in your inventory or playbook:

```yaml
vars:
  keepass_dbx: "/path/to/your/Passwords.kdbx"
  # It's good idea to set vars below via command line while executing ansible-playbook
  # Like ansible-playbook ... -e keepassxc_pwd=my_secret_pass
  keepassxc_pwd: "your_master_password"
  # keepass_key: "/path/to/your/keyfile"   # if applicable
```

## Thanks

Want to thank contributors of [viczem/ansible-keepass](https://github.com/viczem/ansible-keepass).
They did this plugin first but in a different way, that's why I decided "reinvent the bike". 
All their ideas was brazenly stolen and reimplemented by LLM (and me, of course). 
