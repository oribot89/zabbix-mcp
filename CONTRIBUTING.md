# Contributing to Zabbix MCP

Thank you for your interest in contributing to Zabbix MCP! We welcome contributions from the community.

## License

**IMPORTANT**: This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

By contributing to this project, you agree that:
- All contributions must be distributed under GPLv3
- You give credit to the original authors
- You share all derivative works under the same GPLv3 license
- You provide source code for any modifications

See [LICENSE](LICENSE) for the full license text.

## How to Contribute

### Reporting Issues
1. Check existing issues first
2. Provide clear description of the bug
3. Include steps to reproduce
4. Add your Zabbix and Python versions
5. Share error logs/screenshots if relevant

### Submitting Code

1. **Fork the repository**
   ```bash
   gh repo fork oribot89/zabbix-mcp --clone
   cd zabbix-mcp
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add docstrings to functions
   - Update tests if applicable
   - Update README if needed

4. **Test your changes**
   ```bash
   python -m pytest
   python test_connection.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "feat: describe your change clearly"
   ```

6. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Ensure PR includes**
   - Clear description of changes
   - Reference to any related issues
   - Confirmation that code follows GPLv3

## Code Style

- Use Python 3.9+
- Follow PEP 8 conventions
- Use type hints where possible
- Add docstrings to all functions
- Keep functions small and focused

## Testing

All contributions should include tests:
```bash
python -m pytest tests/
```

## Derivative Works

If you create a derivative work (fork, modification, or service using this code):
- You **must** publish the source code
- You **must** license it under GPLv3
- You **must** give credit to original authors
- You **must** provide source code to your users

This is the essence of the GPLv3 license - it keeps software free.

## Questions?

- Open an issue for feature discussions
- Check existing documentation
- Review similar MCP servers for patterns

## Acknowledgments

Contributors are credited in:
- Commit history
- CONTRIBUTORS.md (if added by maintainers)
- Release notes

Thank you for making Zabbix MCP better! 🚀
