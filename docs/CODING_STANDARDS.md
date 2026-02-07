# Coding Standards for MAC Address Converter

## General Principles

### No Emojis in Code
- **Never use emojis in source code** unless explicitly requested by the project owner
- This includes:
  - Variable names
  - Function names
  - Comments within code
  - String literals used in UI elements
  - Log messages
  - Error messages

### Code Style
- Follow PEP 8 for Python code
- Use clear, descriptive variable and function names
- Keep functions focused on a single responsibility
- Add docstrings for functions and classes

### Documentation
- README and documentation files may use emojis for visual appeal
- Code documentation should be emoji-free and professional

### UI Text
- UI labels and buttons should use plain text
- Icons should be implemented using proper icon libraries, not emoji characters
- Exception: If emojis are part of the design requirements or explicitly requested

## Project-Specific Standards

### Tkinter GUI
- Use modern, flat design principles
- Maintain consistent color scheme defined in COLORS dictionary
- All interactive elements should have hover states
- Use proper fonts (Segoe UI for text, Consolas for monospace)

### Clipboard Handling
- Always use Tkinter's native clipboard methods (`clipboard_get()`, `clipboard_append()`)
- Never use external libraries like pyperclip that may cause focus stealing on Linux

### Performance
- Keep clipboard polling at 500ms intervals
- Use Tkinter's `after()` method instead of threading for periodic tasks
- Minimize dependencies to keep executable size small

### Cross-Platform Compatibility
- Test on Linux, Windows, and macOS before releases
- Use platform-agnostic code where possible
- Document platform-specific requirements clearly

## Examples

### ❌ Bad (Emoji in code)
```python
def convert_case():
    button = tk.Button(text="🔄 Convert Case")
```

### ✅ Good (No emoji in code)
```python
def convert_case():
    button = tk.Button(text="Convert Case")
```

## Enforcement

These standards should be followed by:
- All contributors
- AI assistants working on the codebase
- Code reviews should check for compliance
