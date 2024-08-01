# content_manager

This repository contains the source code for HackyAIMod, an AI-based content moderation tool.

## Deployment

### Using Docker

1. **Download the Dockerfile from the repository:**
    [Dockerfile](https://github.com/Aakashjammula/content_manager/tree/main)
2. **Build the Docker image:**
    ```sh
    docker build -t HackyAI .
    ```
3. **Turn off access control for Docker to your X11 server:**
    ```sh
    xhost +local:docker
    ```
4. **Run the Docker container:**
    - **If you have an Nvidia GPU installed:**
        ```sh
        docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY --security-opt=label=disable --runtime=nvidia -d --name content_manager -i HackyAI
        ```
    - **If you don't have an Nvidia GPU installed:**
        ```sh
        docker run --security-opt=label=disable -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -d --name content_manager -i HackyAI
        ```

### Without using Docker [Recommended]

1. **Recommended Python Version:** 3.11.x

2. **Clone the git repository:**
    ```sh
    git clone https://github.com/Aakashjammula/content_manager
    ```

3. **Install required dependencies from `requirements.txt`:**
    ```sh
    cd content_manager
    pip install -r requirements.txt
    ```

4. **To test the model, use the following command:**
    ```sh
    python test_model.py
    ```

5. **To test the Chat UI, use the following command:**
    ```sh
    python test_ui.py
    ```

## Repository Structure

- `Dockerfile`: Contains the Docker configuration for the project.
- `requirements.txt`: Lists the dependencies required for the project.
- `test_model.py`: Script to test the AI model.
- `test_ui.py`: Script to test the Chat UI.

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
