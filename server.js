const express = require("express");

const app = express();
const PORT = process.env.PORT || 3000;
const startTime = Date.now();

app.use(express.json());

// --- Default device states ---

const DEFAULT_DEVICES = [
  { id: "light-1", name: "Living Room Light", type: "Light", on: false, brightness: 100 },
  { id: "light-2", name: "Bedroom Light", type: "Light", on: false, brightness: 75 },
  { id: "thermostat-1", name: "Main Thermostat", type: "Thermostat", on: true, temperature: 72 },
  { id: "lock-1", name: "Front Door Lock", type: "Lock", locked: true },
  { id: "lock-2", name: "Back Door Lock", type: "Lock", locked: true },
];

function cloneDefaults() {
  return JSON.parse(JSON.stringify(DEFAULT_DEVICES));
}

let devices = cloneDefaults();

// --- Routes ---

// Health check
app.get("/health", (_req, res) => {
  res.json({ status: "ok", uptime: Math.floor((Date.now() - startTime) / 1000) });
});

// List all devices
app.get("/devices", (_req, res) => {
  res.json(devices);
});

// Get a single device
app.get("/devices/:id", (req, res) => {
  const device = devices.find((d) => d.id === req.params.id);
  if (!device) {
    return res.status(404).json({ error: `Device '${req.params.id}' not found` });
  }
  res.json(device);
});

// Update a device
app.patch("/devices/:id", (req, res) => {
  const device = devices.find((d) => d.id === req.params.id);
  if (!device) {
    return res.status(404).json({ error: `Device '${req.params.id}' not found` });
  }

  const allowedFields = {
    Light: ["on", "brightness"],
    Thermostat: ["on", "temperature"],
    Lock: ["locked"],
  };

  const fields = allowedFields[device.type] || [];
  const updates = req.body;

  if (!updates || typeof updates !== "object" || Object.keys(updates).length === 0) {
    return res.status(400).json({ error: "Request body must be a non-empty JSON object" });
  }

  const invalid = Object.keys(updates).filter((k) => !fields.includes(k));
  if (invalid.length > 0) {
    return res.status(400).json({
      error: `Invalid fields for ${device.type}: ${invalid.join(", ")}`,
      allowed: fields,
    });
  }

  Object.assign(device, updates);
  res.json(device);
});

// Reset all devices to defaults
app.post("/reset", (_req, res) => {
  devices = cloneDefaults();
  res.json({ message: "All devices reset to default state" });
});

// --- Start server ---

app.listen(PORT, () => {
  console.log(`Smart Home API running on http://localhost:${PORT}`);
});
