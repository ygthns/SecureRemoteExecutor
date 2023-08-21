# SecureRemoteExecutor
This agent provides a secure interface for executing whitelisted commands on remote servers. It is designed with security in mind, using HTTPS and token-based authentication to ensure that only authorized clients can execute commands. The agent logs command execution in a human-readable format and can be easily integrated into various environments.

## Features

- **IP Whitelisting**: Only requests from a specific IP address are allowed.
- **Token-based Authentication**: A pre-shared API token is required to execute commands.
- **Command Whitelisting**: Only predefined command prefixes are allowed.
- **Path Blacklisting**: Specific paths and arguments can be blacklisted to prevent unauthorized actions.
- **Encrypted Communication**: Uses HTTPS to encrypt communication between the client and the agent.

## Dependencies

- Python 3.x
- Flask
- Requests (if using the Python client script)

## Installation

1. Clone the repository.
2. Install the required Python packages:

   ```bash
   pip install flask requests
   ```

3. Generate self-signed certificates for HTTPS:

   ```bash
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```

   Place the generated `cert.pem` and `key.pem` files in the same directory as the agent.

## Usage

### Starting the Agent

Run the agent using the following command:

```bash
python agent.py
```

The agent will start listening on port 5000.

### Executing Commands from a Remote Server

#### Using `curl`:

```bash
curl -k -X POST https://AGENT_IP:5000/execute \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-secure-api-token-here" \
     -d '{"command": "/etc/init.d/hpcc-init restart"}'
```

#### Using Python:

```python
import requests

url = "https://AGENT_IP:5000/execute"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-secure-api-token-here",
}
data = {
    "command": "/etc/init.d/your-script restart",
}

response = requests.post(url, json=data, headers=headers, verify=False)

print(response.json())
```

## Security Considerations

- Store the certificates and API token securely.
- Only use trusted networks for communication between the client and agent.
- Consider using a recognized Certificate Authority (CA) to sign the certificates.
- Continuously monitor the agent logs for any suspicious activity.

## Contributing

Feel free to open issues or submit pull requests with improvements or bug fixes.
