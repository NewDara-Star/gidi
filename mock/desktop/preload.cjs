// Tells the page it is running as the Gidi desktop app.
const { contextBridge } = require("electron");
contextBridge.exposeInMainWorld("gidiDesktop", { platform: process.platform, version: "0.1.0" });
