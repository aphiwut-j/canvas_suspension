# Canvas User Suspension Tool

This Python GUI tool allows administrators to suspend Canvas users efficiently. With an easy-to-use interface, users can manage suspensions without needing to interact directly with the backend.

## Dependencies

Before running the tool, ensure the following dependencies are installed:
- `requests`: For making HTTP requests to the Canvas API.
- `pandas`: For data handling and manipulation.
- `tkinter`: For creating the GUI.

You can install these dependencies using pip:

```bash
pip install requests pandas
```

`tkinter` is included with standard Python installations on most systems.

## Setup Instructions

To use the tool, you'll need to configure the `token_canvas` module. Follow these steps:

1. Obtain your Canvas API token.
2. Create a file named `token_canvas.py` in the same directory as the tool.
3. Add the following code to `token_canvas.py`:

   ```python
   TOKEN = 'your_canvas_api_token_here'
   ```

Replace `'your_canvas_api_token_here'` with your actual API token.

## Usage Workflow

1. Run the tool:
   ```bash
   python canvas_suspension_tool.py
   ```
2. Load your input data file using the GUI.
3. Follow the on-screen instructions to suspend users.
4. Review any output logs for the actions taken.

## File Format Requirements

The input file must be in CSV format with the following columns:
- `user_id`
- `user_name`
- Any other fields required by the tool.

Ensure the CSV file is well-formed to avoid errors during processing.

## API Information

The tool communicates with the Canvas API to manage user suspensions. Refer to the [Canvas API documentation](https://lms.au.af.edu/doc/api/all_resources.html) for more information on available endpoints and functionality.
