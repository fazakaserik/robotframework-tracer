import * as vscode from 'vscode';
import * as listenermanager from './ListenerManager';
import * as pythonmanager from './PythonManager';

export function activate(context: vscode.ExtensionContext) {
	const config = vscode.workspace.getConfiguration(context.extension.id);
	const result = config.get("robotframeworkTracer.display.primaryLocation");
	console.log(result);
	pythonmanager.activate(context);
	listenermanager.activate(context);
}

export function deactivate() {
	listenermanager.deactivate();
	pythonmanager.deactivate();
}
