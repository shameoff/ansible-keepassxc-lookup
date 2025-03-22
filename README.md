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

### Install KeePassXC

See [KeePassXC site](https://keepassxc.org/) for details of Installation.  
In my case installing it via `apt install keepassxc` was enough. I'm sure, other package managers
also have this package

### Install plugin via Ansible Galaxy

```bash
ansible-galaxy collection install shameoff.keepassxccli
```

### Install plugin manually 
If you want to store plugins near with your ansible-playbooks, do next:

1. Create/Edit an `ansible.cfg` file and add in defaults section the string `lookup_plugins=./plugins/lookup`

```ini
[defaults]
lookup_plugins=./plugins/lookup
... # other params
```

2. Paste the file `plugins/lookup/keepassxccli.py` in `./plugins/lookup`

## Usage

### Before usage

- Set the following variables in your inventory or playbook:
  - `keepassxc_kdbx_path`: Path to the KeePass database file.
  - `keepassxc_pwd`: Master password for the KeePass database.
  - Optionally, `keepassxc_key_file`: Path to the key file if used.

Or, alternatively, you can set environment variables:

- `ANSIBLE_KEEPASSXC_PWD` Password
- `ANSIBLE_KEEPASSXC_KEY_FILE` Path to keyfile

In your playbook, you can use the lookup plugin like this:

```yaml
- name: Retrieve password from KeePass
  debug:
    msg: "{{ lookup('shameoff.keepassxccli.keepassxccli', 'A_name_of_your_credentials_entity', 'password') }}"

- name: Retrieve a custom property from KeePass
  debug:
    msg: "{{ lookup('shameoff.keepassxccli.keepassxccli', 'Entry (can contain spaces)', 'custom_properties', 'my_prop_key') }}"
```

> [!TIP]
> Pay attention, that if you install plugin manually in your `lookup_plugins` folder, you should call it like `keepassxccli` instead of `shameoff.keepassxccli.keepassxccli`

Ensure that the required variables are defined, for example in your inventory or playbook:

```yaml
vars:
  keepassxc_kdbx_path: "/path/to/your/Passwords.kdbx"
  # It's good idea to set vars below via command line while executing ansible-playbook
  # Like ansible-playbook ... -e keepassxc_pwd=my_secret_pass
  keepassxc_pwd: "your_master_password"
  # keepassxc_key_file: "/path/to/your/keyfile"   # if applicable
```

## Thanks

Want to thank contributors of [viczem/ansible-keepass](https://github.com/viczem/ansible-keepass).
They did this plugin first but in a different way, that's why I decided "reinvent the bike".
All their ideas was brazenly stolen and reimplemented by LLM (and me, of course).
