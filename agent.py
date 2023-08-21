from flask import Flask, request, jsonify
import subprocess
import logging
import re
import uuid

# Allowed IP address (your application server)
ALLOWED_IP = "192.168.1.10"
# Pre-shared API token for authentication
API_TOKEN = "your-secure-api-token-here"
# Allowed command prefixes
ALLOWED_PREFIXES = ["/etc/init.d/my-custom-script", "/bin/ls", "/bin/mkdir"]  # Define allowed command prefixes here
# Blacklisted arguments or paths
BLACKLISTED_ARGUMENTS = ["/etc/", "/var/", "/usr/"]  # Define disallowed arguments or paths here

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename="agent.log", level=logging.INFO)

def log_command_result(command, result):
    logging.info(f"""
        ID: {uuid.uuid4()}
      Name: {command.split()[0]}
     State: COMPLETE
       PID: {result.pid}
 StartTime: {result.args}
  StopTime: {result.returncode}
  ExitCode: {result.returncode}
     Error: {result.stderr.decode('utf-8') if result.returncode != 0 else ""}
    Stdout:
{result.stdout.decode('utf-8')}
    Stderr: {result.stderr.decode('utf-8')}
    """)

@app.route('/execute', methods=['POST'])
def execute_command():
    client_ip = request.remote_addr
    token = request.headers.get("Authorization")

    # Validate IP address and token
    if client_ip != ALLOWED_IP or token != "Bearer " + API_TOKEN:
        logging.warning(f"Unauthorized access attempt from {client_ip}")
        return jsonify({"error": "Unauthorized access"}), 403

    command = request.json.get("command")
    if not command or not any(command.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        logging.warning(f"Invalid or unauthorized command requested: {command}")
        return jsonify({"error": "Invalid or unauthorized command"}), 400

    # Check for blacklisted arguments or paths
    if any(arg in command for arg in BLACKLISTED_ARGUMENTS):
        logging.warning(f"Blacklisted argument detected in command: {command}")
        return jsonify({"error": "Unauthorized argument or path in command"}), 403

    # Execute the command
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    log_command_result(command, result)  # Log the result

    response_data = {
        "stdout": result.stdout.decode('utf-8'),
        "stderr": result.stderr.decode('utf-8'),
        "returncode": result.returncode
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
