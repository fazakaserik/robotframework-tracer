import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";
import * as os from "os";

function getResolvedConfig(section: string): { [key: string]: any } {
  const config = vscode.workspace.getConfiguration(section);
  const configKeys = Object.keys(config).filter((key) => {
    // Filter out methods and only keep configuration properties
    return typeof config[key] !== "function";
  });

  const resolvedConfig: { [key: string]: any } = {};

  configKeys.forEach((key) => {
    const inspected = config.inspect(key);
    if (inspected) {
      resolvedConfig[key] = resolveConfigValue(inspected);
    }
  });

  return resolvedConfig;
}

function resolveConfigValue(inspected: any): any {
  if (
    typeof inspected.defaultValue === "object" &&
    !Array.isArray(inspected.defaultValue)
  ) {
    // Handle nested configuration objects
    const resolvedNestedConfig: { [key: string]: any } = {};
    const nestedKeys = Object.keys(inspected.defaultValue);

    nestedKeys.forEach((nestedKey) => {
      const nestedInspected = {
        defaultValue: inspected.defaultValue[nestedKey],
        globalValue: inspected.globalValue
          ? inspected.globalValue[nestedKey]
          : undefined,
        workspaceValue: inspected.workspaceValue
          ? inspected.workspaceValue[nestedKey]
          : undefined,
      };

      resolvedNestedConfig[nestedKey] = resolveConfigValue(
        nestedInspected as any
      );
    });

    return resolvedNestedConfig;
  } else {
    // Handle simple values
    if (inspected.workspaceValue !== undefined) {
      return inspected.workspaceValue;
    } else if (inspected.globalValue !== undefined) {
      return inspected.globalValue;
    } else {
      return inspected.defaultValue;
    }
  }
}

function exportConfig(context: vscode.ExtensionContext) {
  const config = vscode.workspace.getConfiguration("robotFrameworkTracer");
  const configKeys = Object.keys(config).filter((key) => {
    // Filter out methods and only keep configuration properties
    return typeof config[key] !== "function";
  });

  const resolvedConfig = getResolvedConfig("robotFrameworkTracer");

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

export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand(
    "robot-framework-tracer.updateConfigs",
    () => {
      exportConfig(context);
      vscode.window.showInformationMessage(
        "Robot Framework Tracer configurations have been updated."
      );
    }
  );

  context.subscriptions.push(disposable);

  exportConfig(context);
}

export function deactivate() {}
