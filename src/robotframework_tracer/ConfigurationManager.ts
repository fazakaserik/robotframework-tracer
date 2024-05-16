import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";
import * as os from "os";

export function activate(context: vscode.ExtensionContext) {
  const config = vscode.workspace.getConfiguration("robotFrameworkTracer");

  const settings = {
    executionTrace: {
      enabled: config.get("executionTrace.enabled"),
      location: config.get("executionTrace.location"),
    },
    mouseTrace: {
      enabled: config.get("mouseTrace.enabled"),
      maxMouseClicksRecorded: config.get("mouseTrace.maxMouseClicksRecorded"),
    },
  };

  const settings_json = JSON.stringify(settings, null, 4);

  // Generate a temporary file path
  const tempDir = os.tmpdir();
  const filePath = path.join(tempDir, "robotframework-tracer-settings.json");

  // Write settings to the temporary file
  fs.writeFile(filePath, settings_json, (err) => {
    if (err) {
      vscode.window.showErrorMessage(
        "Error exporting settings: " + err.message
      );
      return;
    }
    console.log("Settings exported to " + filePath);
  });
}

export function deactivate() {}
