# Contributing to This Project

We welcome contributions to improve this project! Please take a moment to review these guidelines.

## How to Contribute

*   **Reporting Bugs:** If you find a bug, please open an issue on the project's issue tracker (e.g., GitHub Issues), providing as much detail as possible, including steps to reproduce.
*   **Suggesting Enhancements:** For new features or enhancements, please open an issue to discuss your ideas before submitting code.
*   **Pull Requests:** Contributions are primarily made via Pull Requests (PRs).

## Development Guidelines

*   **Set up your Development Environment:** Follow the setup instructions in `README.md` to create a virtual environment and install dependencies.
*   **Coding Standards:**
    *   **Formatting:** This project uses `black` for code formatting. Please format your code using `python -m black .` before committing.
    *   **Linting:** `flake8` is used for linting. Ensure your code passes `python -m flake8 .` (respecting the project's `.flake8` configuration).
    *   **Pre-commit Hooks:** It's recommended to install and use the pre-commit hooks configured in `.pre-commit-config.yaml` to automate these checks.
*   **Testing:**
    *   Write new unit tests for any new features or bug fixes.
    *   Ensure all tests pass (`python -m pytest`) before submitting a PR.
*   **Documentation:**
    *   Update documentation (e.g., `README.md`, files in `docs/`) as needed to reflect your changes.
    *   Comment your code where necessary for clarity.
*   **Commit Messages:** Write clear and concise commit messages.

## Submitting Changes

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes, adhering to the guidelines above.
4.  Commit your changes and push them to your fork.
5.  Open a Pull Request against the main repository.

Thank you for contributing!
