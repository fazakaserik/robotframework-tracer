import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";
import * as cp from "child_process";
import {
  PythonExtension,
  ActiveEnvironmentPathChangeEvent,
} from "@vscode/python-extension"; // https://github.com/d-biehl/robotcode/blob/main/vscode-client/pythonmanger.ts

async function checkPythonPackages(
  context: vscode.ExtensionContext
): Promise<void> {
  const pythonExtension = vscode.extensions.getExtension("ms-python.python");
  if (!pythonExtension) {
    vscode.window.showErrorMessage("Python extension is not installed");
    return;
  }

  if (!pythonExtension.isActive) {
    await pythonExtension.activate();
  }

  // https://github.com/microsoft/vscode-python/blob/main/src/client/deprecatedProposedApi.ts
  let activePythonEnvironment;
  // Check if the Python extension's exported API has the method we need
  if (pythonExtension.exports && pythonExtension.exports.environment) {
    try {
      activePythonEnvironment =
        await pythonExtension.exports.environment.getEnvironmentDetails(
          (
            await pythonExtension.exports.environment.getActiveEnvironmentPath()
          ).path
        );
    } catch (error) {
      console.error("Failed to get the active Python environment path:", error);
    }
  } else {
    vscode.window.showErrorMessage(
      "Python extension does not support the required API."
    );
  }

  const requirementsPath = path.join(context.extensionPath, "requirements.txt");
  if (!fs.existsSync(requirementsPath)) {
    vscode.window.showErrorMessage("requirements.txt file not found.");
    return;
  }

  const requirements = fs
    .readFileSync(requirementsPath, "utf-8")
    .split("\n")
    .filter((line) => line.trim() !== "");

  let missingPackages: string[] = [];
  for (const requirement of requirements) {
    try {
      let requirementName = requirement.split("==")[0];
      cp.execSync(
        `${activePythonEnvironment.interpreterPath} -m pip show ${requirementName}`,
        { encoding: "utf-8" }
      );
    } catch {
      missingPackages.push(requirement);
    }
  }

  if (missingPackages.length > 0) {
    const installMsg = `The following python packages are missing: ${missingPackages.join(
      ", "
    )}. Install now?`;
    const choice = await vscode.window.showInformationMessage(
      installMsg,
      "Yes",
      "No"
    );
    if (choice === "Yes") {
      installPythonPackages(
        activePythonEnvironment.interpreterPath,
        missingPackages
      );
    } else {
      vscode.window.showErrorMessage(
        "Required Python packages were not installed."
      );
    }
  } else {
    vscode.window.showInformationMessage(
      "All required Python packages are installed."
    );
  }
}

function installPythonPackages(pythonPath: string, packages: string[]): void {
  vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: "Installing Python packages",
      cancellable: true,
    },
    (progress, token) => {
      const cmd = `${pythonPath} -m pip install ${packages.join(" ")}`;
      return new Promise<void>((resolve, reject) => {
        cp.exec(cmd, (error, stdout, stderr) => {
          if (error) {
            vscode.window.showErrorMessage(
              `Failed to install packages: ${stderr}`
            );
            reject();
          } else {
            vscode.window.showInformationMessage(
              "Python packages installed successfully."
            );
            resolve();
          }
        });
      });
    }
  );
}

export function activate(context: vscode.ExtensionContext) {
  checkPythonPackages(context);
}

export function deactivate() {}
