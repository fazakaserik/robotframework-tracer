import * as vscode from 'vscode';

const LISTENER_FLAG = "--listener";
const LISTENER_VALUE = "ListenerClass.py";

const ROBOT_EXTENSION = "robotcode";
const ROBOT_EXTENSION_SETTING = 'robot.args';

function setListener(context: vscode.ExtensionContext, config: vscode.WorkspaceConfiguration, listener: string): void {
	let updateArgs = config.get<string[]>(ROBOT_EXTENSION_SETTING) || [];
    const hasListener = updateArgs.some(arg => arg.startsWith(`${LISTENER_FLAG}=`)) || false;

    if (hasListener) {
        updateArgs = updateArgs.map(arg => arg.startsWith(`${LISTENER_FLAG}=`) ? `${LISTENER_FLAG}=${listener}` : arg);
    } else {
        updateArgs.push(`${LISTENER_FLAG}=${listener}`);
    }
    
	config.update(ROBOT_EXTENSION_SETTING, updateArgs, vscode.ConfigurationTarget.Workspace)
        .then(() => {
            vscode.window.showInformationMessage(`Set ${context.extension.packageJSON.displayName} as RobotCode listener.`);
        }, error => {
            vscode.window.showErrorMessage(`Error updating RobotCode settings: ${error}`);
        });
}

function updateListener(context: vscode.ExtensionContext): void {
	const robot_extension_config = vscode.workspace.getConfiguration(ROBOT_EXTENSION);

	const args = robot_extension_config.get<string[]>(ROBOT_EXTENSION_SETTING);
    const hasListener = args?.some(arg => arg.startsWith(`${LISTENER_FLAG}=`)) || false;

    if (!hasListener) {
        setListener(context, robot_extension_config, LISTENER_VALUE);
        return;
    }

    const listenerAlreadySet = args?.some(arg => arg === `${LISTENER_FLAG}=${LISTENER_VALUE}`) || false;

    if (listenerAlreadySet) {
        return;
    }

    vscode.window.showInformationMessage(
        `Allow ${context.extension.packageJSON.displayName} to change the RobotCode listener?`,
        'Yes',
        'No'
    ).then(choice => {
        if (choice === "Yes") {
            setListener(context, robot_extension_config, LISTENER_VALUE);
        } else {
            vscode.window.showErrorMessage(`${context.extension.packageJSON.displayName} listener was not set, thus it won't be active.`);
        }
    });
}

export function activate(context: vscode.ExtensionContext) {
    // When the extension loads, check if the listener is set
	updateListener(context);

	// Otherwise provide a command to set it
	let disposable = vscode.commands.registerCommand('robot-framework-tracer.updateListener', () => {
        updateListener(context);
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {
	const robot_extension_config = vscode.workspace.getConfiguration(ROBOT_EXTENSION);

	let updateArgs = robot_extension_config.get<string[]>(ROBOT_EXTENSION_SETTING);
    updateArgs = updateArgs?.filter(arg => !arg.startsWith("--listener="));
	robot_extension_config.update(ROBOT_EXTENSION_SETTING, updateArgs, vscode.ConfigurationTarget.Workspace);
}
