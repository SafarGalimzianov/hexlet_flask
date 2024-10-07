

# Docker Engine Installation

## Add Docker's official GPG key:

1. **Update the package list:**
    ```sh
    sudo apt-get update
    ```

2. **Install required packages:**
    ```sh
    sudo apt-get install ca-certificates curl
    ```

3. **Create the directory for the keyring:**
    ```sh
    sudo install -m 0755 -d /etc/apt/keyrings
    ```
    - `-m 0755`: Sets the directory permissions to `0755` (read, write, and execute for the owner, and read and execute for others).
    - [`-d`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsafar%2Fhexlet%2Fhexlet_flask%2FMakefile%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A23%2C%22character%22%3A3%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsafar%2Fhexlet%2Fhexlet_flask%2Fpoetry.lock%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A93%2C%22character%22%3A17%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsafar%2Fhexlet%2Fhexlet_flask%2Fpoetry.lock%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A229%2C%22character%22%3A14%7D%7D%5D%2C%226c76e152-85f9-4db7-b872-dbb7ca570dbf%22%5D "Go to definition"): Creates the directory if it does not exist.

4. **Download Docker's GPG key:**
    ```sh
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    ```
    - `-f`: Fail silently on server errors.
    - `-s`: Silent mode.
    - `-S`: Show errors.
    - `-L`: Follow redirects.
    - [`-o`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsafar%2Fhexlet%2Fhexlet_flask%2Fpoetry.lock%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A5%2C%22character%22%3A37%7D%7D%5D%2C%226c76e152-85f9-4db7-b872-dbb7ca570dbf%22%5D "Go to definition"): Write output to the specified file.

5. **Set the appropriate permissions for the keyring:**
    ```sh
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    ```
    - `a+r`: Adds read permission for all users.

## Add the repository to Apt sources:

1. **Add Docker's repository:**
    ```sh
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```
    - `arch=$(dpkg --print-architecture)`: Specifies the architecture.
    - `signed-by=/etc/apt/keyrings/docker.asc`: Uses the specified keyring for signing.
    - `$(. /etc/os-release && echo "$VERSION_CODENAME")`: Gets the codename of the current Ubuntu version.
    - `sudo tee /etc/apt/sources.list.d/docker.list`: Writes the output to the specified file.
    - `> /dev/null`: Discards the standard output.

2. **Update the package list again:**
    ```sh
    sudo apt-get update
    ```

By following these steps, you will add Docker's official GPG key and repository to your system, allowing you to install Docker Engine.

# Docker APT
The Docker APT repository is a location where Debian-based systems can obtain the Docker software packages via the APT (Advanced Package Tool) package management system, simplifying the installation and management of Docker.

Understanding Docker: Docker is an open-source platform that enables developers to automate the deployment of applications in lightweight, portable containers. Containers package an application with its dependencies, making it easier to run consistently across different environments.

APT Overview: APT, or Advanced Package Tool, is a powerful package management system used by Debian and Ubuntu-based systems. It allows users to install, update, and manage software packages efficiently.

What is an APT Repository?: An APT repository is a storage location from which software packages can be retrieved and installed using the APT tool. It contains a set of packages and metadata that helps APT understand which packages are available, their dependencies, and how to install them.

Docker APT Repository:

    The Docker APT repository specifically hosts Docker software packages for Debian and Ubuntu-based distributions. It simplifies the process of installing Docker on these systems.
    By adding the Docker APT repository to your system’s package source list, you can easily install Docker using standard APT commands (e.g., apt-get install docker-ce).

# Docker Desktop
systemctl --user start docker-desktop
systemctl --user enable docker-desktop
systemctl --user stop docker-desktop

