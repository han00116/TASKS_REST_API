# Import required libraries
from flask import Flask, jsonify, request

# Sample data: a list of tasks
tasks = [
    {
        'id': 1,
        'title': 'Learn Flask',
        'done': False
    },
    {
        'id': 2,
        'title': 'Develop REST API',
        'done': False
    }
]

# Create a Flask application instance
app = Flask(__name__)

# Route for the root of the application
@app.route('/')
def hello():
    # Just returns a welcome message
    return "Hello. Task API is Live!"

# Endpoint to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Convert the tasks data to JSON format and return it
    return jsonify({'tasks': tasks})

# Endpoint to get a specific task by its ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Initialize the task variable as None
    task = None
    # Loop through the tasks list
    for t in tasks:
        if t["id"] == task_id:  # If the task with the given ID is found
            task = t
            break
    # If task is not found after looping
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    # Return the found task
    return jsonify({'task': task})

# Endpoint to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    # Parse the 'done' status from request, default to False if it's not provided
    status = request.json.get('done', False)
    # Convert potential string value "true" to boolean True
    status = status.lower() == "true"

    # Create a new task object
    new_task = {
        'id': len(tasks) + 1,  # Set ID as the next number in sequence
        'title': request.json['title'],  # Get the title from request data
        'done': status  # Set the parsed status
    }

    # Add the new task to the tasks list
    tasks.append(new_task)

    # Return the added task with a status code indicating resource creation
    return jsonify({'task': new_task}), 201

# Endpoint to update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Initialize the task variable as None
    task = None
    # Loop through the tasks list
    for t in tasks:
        if t["id"] == task_id:  # If the task with the given ID is found
            task = t
            break
    # If task is not found after looping
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    # Update task attributes with data from the request, use existing value if not provided
    task['title'] = request.json.get('title', task['title'])
    task['done'] = request.json.get('done', task['done'])
    # Return the updated task
    return jsonify({'task': task})

# Endpoint to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks  # Reference the global tasks list
    # Initialize the task variable as None
    task = None
    # Loop through the tasks list
    for t in tasks:
        if t["id"] == task_id:  # If the task with the given ID is found
            task = t
            break
    # If task is not found after looping
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    # Remove the found task from the tasks list
    tasks.remove(task)
    # Return a success message
    return jsonify({'result': 'Task deleted successfully'}), 200

# This is the entry point of the application
if __name__ == '__main__':
    # Start the Flask development server with debugging enabled
    app.run(debug=True)
