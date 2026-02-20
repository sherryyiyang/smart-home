Prompt:
"I need a simple Node.js Express backend for testing my E2E tool.

** Requirements: **

No Database: Use a global JavaScript object/array to store state in memory.

Theme: A 'Smart Home Control' API.

Endpoints:
GET /health: Returns { "status": "ok", "uptime": 123 }.
GET /devices: Returns a list of devices (Light, Thermostat, Lock) and their current states.
PATCH /devices/:id: Updates the state of a specific device (e.g., toggle 'on' to 'off').
POST /reset: Resets all device states to their default (crucial for E2E test cleanup).

Validation: Include basic error handling (e.g., 404 if device ID doesn't exist).

Deployment Ready: Include a simple Dockerfile and a start script in package.json.

Please keep the code in a single server.js file for simplicity."