# Udacity Full Stack Nanodegree Project - Item Catalog
Submission for [Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)'s *Item Catalog* Project. The project tests the developer's skill in applying authorisation, servers and CRUD knowledge using a Flask web application.

## Project Overview
An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Get Started

Follow these steps to run the project. You must use a terminal (command line interface):

### Step 1: Set up the virtual machine
1. **Install VirtualBox**
    
    You can [download it from virtualbox.org, here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system.

2. **Install Vagrant**
    
    Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

3. **Download the VM Configuration**
    
    Fork and clone the  [Fullstack Nanodegree VM Repo](https://github.com/udacity/fullstack-nanodegree-vm). Open up your terminal and then `cd` into the directory. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory. 
    
    [*How to Fork a Repository*](https://help.github.com/articles/fork-a-repo/)

4. **Start the virtual machine**
    
    From inside the **vagrant** directory run the following command:
    ```bash
    vagrant up
    ```
    After that is completed run the following command to login to the virtual machine:
    ```bash
    vagrant ssh
    ```
### Step 2: Set Up Google Authentication Prerequisites
This project uses Google Accounts to implement authentication, a [hybrid OAuth approach](https://developers.google.com/identity/sign-in/web/server-side-flow) . Therfore you must create a client ID and client secret that can be used in the application.

1. Go to the [Google API Console](https://console.developers.google.com/project/_/apiui/apis/library)
2. From the project drop-down, select an existing project, or create a new one by selecting **Create a new project**.
3. In the sidebar under "APIs & Services", select Credentials, then select the OAuth consent screen tab. Choose an Email Address, specify a Product Name, and press Save.
4. In the Credentials tab, select the Create credentials drop-down list, and choose OAuth client ID. Under Application type, select Web application.
5. After creating your credentials, copy the client ID and download the client_secret.json file by going to the Credentials page.

```python
# Replace 'YOUR_CLIENT_ID_HERE' with the copied client ID in login.html line 19

auth2 = gapi.auth2.init({
    client_id: 'YOUR_CLIENT_ID_HERE.apps.googleusercontent.com'
});
```
6. Finally save client_secrets.json inside the ```catalog``` directory
### Step 3: Run the application
5. **Download the code**
    
    Clone this repository to the vagrant directory. Go into the directory and then run:
    ```python
    python database_setup.py
    ```
    This will set up an empty MySQL database by the name itemcatalog.db. To populate the database with some dummy data run:
    ```python
    python populate_db.py
    ```
    After populating the database you can bring up the server and visit the web application on your browser.
    ```python
    python server.py
    ```
    This should open a Flask server at [localhost:5000](http://localhost:5000)