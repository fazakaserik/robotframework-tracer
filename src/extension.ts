import * as vscode from 'vscode';
import * as listenermanager from './ListenerManager';
import * as pythonmanager from './PythonManager';

export function activate(context: vscode.ExtensionContext) {
	pythonmanager.activate(context);
	listenermanager.activate(context);
}

export function deactivate() {
	listenermanager.deactivate();
	pythonmanager.deactivate();
}
