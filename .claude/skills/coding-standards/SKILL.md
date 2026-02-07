# Coding Standards Skill

## Description
Enforces coding standards for this project, with emphasis on professional, clean code without emojis.

## Critical Rules

### No Emojis in Source Code
- **NEVER use emojis in code** unless explicitly requested by the user
- This includes:
  - Variable names
  - Function names
  - Comments within code
  - String literals used in UI elements
  - Log messages
  - Error messages
  - Docstrings

### Code Style
- Follow PEP 8 for Python code
- Use clear, descriptive variable and function names
- Keep functions focused on a single responsibility
- Add docstrings for functions and classes
- Professional, clean code at all times

### UI Text Standards
- UI labels and buttons should use plain text
- No emoji characters in button text or labels
- Icons should be implemented using proper icon libraries, not emoji characters
- Exception: If emojis are explicitly part of design requirements and user requests them

## Project-Specific Standards

### Tkinter GUI Development
- Use modern, flat design principles
- Maintain consistent color scheme defined in COLORS dictionary
- All interactive elements must have hover states
- Use proper fonts:
  - Segoe UI for general UI text
  - Consolas for monospace/technical content

### Clipboard Handling
- Always use Tkinter's native clipboard methods
- Use `window.clipboard_get()` for reading
- Use `window.clipboard_clear()` and `window.clipboard_append()` for writing
- Never use external libraries like pyperclip (causes focus stealing on Linux)

### Performance Guidelines
- Keep clipboard polling at 500ms intervals
- Use Tkinter's `after()` method instead of threading for periodic tasks
- Minimize dependencies to keep executable size small
- Avoid blocking operations

### Cross-Platform Compatibility
- Test on Linux, Windows, and macOS before releases
- Use platform-agnostic code where possible
- Document platform-specific requirements clearly
- Handle platform differences gracefully

## Examples

### Bad - Emoji in code
```python
def convert_case():
    button = tk.Button(text="🔄 Convert Case")
    status = "✅ Success"
```

### Good - No emoji in code
```python
def convert_case():
    button = tk.Button(text="Convert Case")
    status = "Success"
```

### Bad - External clipboard library
```python
import pyperclip
pyperclip.copy(text)
```

### Good - Native Tkinter clipboard
```python
window.clipboard_clear()
window.clipboard_append(text)
window.update()
```

## Enforcement

When working on this project:
1. Check all code changes for emojis before committing
2. Use native Tkinter methods for clipboard operations
3. Follow the established color scheme and styling
4. Maintain cross-platform compatibility
5. Keep code clean, professional, and maintainable

## When to Apply

Apply these standards to:
- All source code files (.py)
- All UI elements
- All documentation within code
- Commit messages (keep professional)

Documentation files (README.md, etc.) may use emojis for visual appeal in user-facing content.
