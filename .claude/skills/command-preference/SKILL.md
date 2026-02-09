# Command Execution Preference

## Critical Rule
NEVER ask the user to run commands manually. ALWAYS run commands directly using the Bash tool.

## Workflow
1. When you need to run a command, ask the user for permission first
2. After receiving approval, run the command using the Bash tool
3. Show the user the output
4. Never provide commands in code blocks for the user to copy and paste

## Examples

### BAD - Don't do this:
```
Run these commands:
```bash
ls -la
```
```

### GOOD - Do this instead:
"I need to check the directory contents. May I run `ls -la`?"

[After user approves]

[Use Bash tool to run the command]

"Here's what I found: [output]"

## Exception
Only provide commands for the user to run manually if they explicitly ask for the commands or if there's a technical reason you cannot run them (e.g., requires sudo password input).
