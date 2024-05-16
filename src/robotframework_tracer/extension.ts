import * as vscode from "vscode";
import * as listenermanager from "./ListenerManager";
import * as pythonmanager from "./PythonManager";
import * as configurationmanager from "./ConfigurationManager";

export function activate(context: vscode.ExtensionContext) {
  pythonmanager.activate(context);
  configurationmanager.activate(context);
  listenermanager.activate(context);
}

export function deactivate() {
  listenermanager.deactivate();
  configurationmanager.deactivate();
  pythonmanager.deactivate();
}
