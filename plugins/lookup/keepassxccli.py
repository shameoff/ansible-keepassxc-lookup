__metaclass__ = type

import os
import subprocess
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

DOCUMENTATION = """
    lookup: keepassxc-cli
    author: Egor Shamov shameoff16@gmail.com
    version_added: '1.0'
    short_description: Fetch data from a KeePass database using keepassxc-cli with enhanced debugging and newline fix
    description:
        - This lookup returns the value of a property of a KeePass entry by invoking keepassxc-cli.
        - It appends a newline to the master password, which might be required by keepassxc-cli.
        - In case of errors, the plugin outputs detailed debug information.
    options:
      _terms:
        description:
          - The first term is the identifier or path to the KeePass entry.
          - The second term is the property name, e.g. username or password.
          - If the property name is 'custom_properties', a third term must be provided, representing the key of the custom property.
        required: True
    notes:
      - Requires keepassxc-cli to be installed and available in the system PATH.
    examples:
      - "{{ lookup('shameoff.keepassxccli.keepassxccli', 'MyEntry', 'username') }}"
      - "{{ lookup('shameoff.keepassxccli.keepassxccli', 'MyEntry', 'password') }}"
      - "{{ lookup('keepassxccli', 'MyEntry', 'custom_properties', 'my_prop_key') }}"
"""

display = Display()


class LookupModule(LookupBase):
    def _var(self, var_value):
        return self._templar.template(var_value, fail_on_undefined=True)

    def run(self, terms, variables=None, **kwargs):
        if not terms:
            raise AnsibleError("KeePassXCCLI: no arguments provided")
        if not all(isinstance(term, str) for term in terms):
            raise AnsibleError("KeePassXCCLI: all arguments must be strings")

        if variables is not None:
            self._templar.available_variables = variables
        variables_ = getattr(self._templar, "_available_variables", {})

        # Get path to the database
        var_dbx = self._var(variables_.get("keepassxc_kdbx_path", ""))
        if not var_dbx:
            raise AnsibleError("KeePassXCCLI: 'keepassxc_kdbx_path' is not set")
        var_dbx = os.path.realpath(os.path.expanduser(os.path.expandvars(var_dbx)))
        if not os.path.isfile(var_dbx):
            raise AnsibleError("KeePassXCCLI: database file '%s' not found" % var_dbx)

        # Get key file (if specified)
        var_key = self._var(variables_.get("keepassxc_key_file", ""))
        if not var_key and "ANSIBLE_KEEPASS_KEY_FILE" in os.environ:
            var_key = os.environ.get("ANSIBLE_KEEPASS_KEY_FILE")
        if var_key:
            var_key = os.path.realpath(os.path.expanduser(os.path.expandvars(var_key)))
            if not os.path.isfile(var_key):
                raise AnsibleError("KeePassXCCLI: key file '%s' not found" % var_key)

        # Get master password
        var_pwd = self._var(variables_.get("keepassxc_pwd", ""))
        if not var_pwd and "ANSIBLE_KEEPASSXC_PWD" in os.environ:
            var_pwd = os.environ.get("ANSIBLE_KEEPASSXC_PWD")
        if not var_pwd:
            raise AnsibleError("KeePassXCCLI: 'keepassxc_pwd' is not set")

        # Process lookup terms: first term - entry identifier, second - property name
        entry_identifier = terms[0]
        if len(terms) < 2:
            raise AnsibleError("KeePassXCCLI: property name is not provided")
        property_name = terms[1]

        # For custom properties, expect a third term with the custom key
        if property_name == "custom_properties":
            if len(terms) < 3:
                raise AnsibleError("KeePassXCCLI: custom property key is not provided")
            attribute = terms[2]
        else:
            attribute = property_name

        # Build the keepassxc-cli command.
        cmd = ["keepassxc-cli", "show", "-a", attribute, var_dbx, entry_identifier]
        if var_key:
            cmd.extend(["--key-file", var_key])

        display.v("KeePassXCCLI: executing command: %s" % " ".join(cmd))

        try:
            # Pass the master password via standard input, appending a newline.
            password_input = (var_pwd + "\n").encode()
            result = subprocess.run(
                cmd, input=password_input, capture_output=True, check=True
            )
            output = result.stdout.decode().strip()
            display.v("KeePassXCCLI: command succeeded, output: %s" % output)
            return [output]
        except subprocess.CalledProcessError as e:
            stdout = e.stdout.decode().strip() if e.stdout else ""
            stderr = e.stderr.decode().strip() if e.stderr else ""
            msg = (
                "Command '%s' returned non-zero exit status %s.\n"
                "STDOUT: %s\nSTDERR: %s"
            ) % (" ".join(cmd), e.returncode, stdout, stderr)
            display.vv("KeePassXCCLI: " + msg)
            raise AnsibleError("KeePassXCCLI: command failed: %s" % msg)
        except Exception as ex:
            msg = "KeePassXCCLI: unexpected error: %s" % str(ex)
            display.vv(msg)
            raise AnsibleError(msg)
