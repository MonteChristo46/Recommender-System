# Recommender-System

Based on the challenge that Data Science is an highly interdisciplinary field of research. This area combines complex methods of 
statistics, mathematics, computer science and machine learning. Nevertheless, the handling of domain-specific data
requires comprehensive domain knowledge. The developed application tries to close the gap between data scientist and 
domain experts. On the one hand the access to the domain specific topic is simplified for the data scientist and on
the other hand the domain expert has an first point of reference for a more comprehensive discussion with the data scientist.  

![](static/img/git/rs.gif)  


## Documentation
A detailed description about all the classes, functions, interfaces and the project structure you'll find in the 
<a target= "_blank" href="http://wwwpub.zih.tu-dresden.de/~s4945549/documentation//html/index.html">documentation</a> of the project.

You can also open the documentation by  downloading the project and navigate yourself to ``static/documentation/Documentation.html`` and open the file in your browser. Otherwise you can also use the link in the footer of the application.


### Notes an pre Requirements

#### Pre Requirements
- Docker version: 18.09.2
- Python version: 3.6.7
- The Docker container: <a href="https://drive.google.com/file/d/18ko3PpT8OYNRWbGQE9_k9THosr03hVME/view?usp=sharing">rs_export.tar</a> (~11GB)
#### Notes
- The docker container as well as the _requirements.txt_ are build on TensorFlow 1.13.0 without(!) GPU support
- If you want GPU support you need to build your own docker image and change the _requirements.txt_
- All squared brackets [] in the following code __are placeholder__ and not part of the command!
- You need to download the <a href ="https://drive.google.com/drive/folders/1wag4iuSkjn2tgzCYdzVbGB4-rkQdeUge?usp=sharing">FastText-Modell</a>
    an include it in the models folder of the project if you want to install the project via pip. 

## Installation

Basically,  you have three ways to install the recommendation system: 

__Recommended Approach:__
1. Basically you can just use the .sh or .bat files of the project to install the software. 
(_We don't guarantee that these will work on every platform!_)

__Other Approaches:__   
2. You can use the docker image (<a href = "https://drive.google.com/file/d/18ko3PpT8OYNRWbGQE9_k9THosr03hVME/view?usp=sharing">rs_export.tar</a>) to load the image and run the container.  
3. You can also set up a python environment and run the program via _app.py_ (_Only recommended for development_)  

In both approaches you need to __download the <a href="https://drive.google.com/drive/folders/1wag4iuSkjn2tgzCYdzVbGB4-rkQdeUge?usp=sharing">FastText model directory</a>__ and copy it in the ``Recommender-System/Models`` 
directory! So it needs to look like that: ``Recommender-System/models/FastText/1/*``

## Installation with the batch/shell files (__Recommended__)
Depending on which operating system you are working you only need to run those files in your terminal. Copy those files
outside of the directory where the rs_export.tar and the Recommender-System directory is stored - the folder structure 
needs to look like followed: 

```
- Dockerfile
- .dockerignore
- rs_export.tar
- run.[bat, sh]
- stop.[bat, sh]
- install.[bat, sh]
- Recommender-System
    - data
    - models
    - ...
```

Please use batch files on windows and shell files on MacOSX/Linux  
1. Run the install.bat and wait for the process to finish

2. Go to localhost:80 in Google Chrome

3. To stop the docker again run stop.bat

4. Step 1 is only for first installation. In future you simply can run run.bat

## Using the Docker Container
The docker consists of all necessary files, libraries and dependencies to start the software - so you don't need to install them. 
Before you start, make sure that you have installed docker (https://docs.docker.com/docker-for-windows/install/). 

1. Follow the steps as described here: <a href="https://docs.docker.com/docker-for-windows/install/">docker installation</a> to install Docker. 
2. Open the terminal and load the docker image: ```docker load --input [PATH TO rs_export.tar] ```  
3. Run the docker ```docker run rs``` (_If it doesn't work go to step 4_) 
4. (Optional) Create a docker container with the name "rs" and run it on port 80: ```docker run --name rs  -p 80:80 rs```

### Some Other Use Full Commands
1. Stop a running container: ```docker stop [NAME OF CONTAINER]``` 
2. Start the docker container again: ```docker start rs```
3. List all containers ``docker ps -a``
4. List all images ``docker images``
5. Delete a container ``docker rm [CONTAINER NAME]``
6. Delete a docker image ``docker image rm [IMAGE NAME]``


## Installation via pip (or conda)
If you don't prefer to use a docker container, you can also install the software to your local python environment. 
We recommend to create a new environment via venv or conda. All required packages are listed in the requirements.txt file. 
__Please make sure that you use at least Python 3.6.7__

1. First update pip: ``pip install --upgrade pip``
2. Install the packages via pip: `` pip install -r [PATH TO requirements.txt]`` 
3. After the installation completed run the following command in your python environment to install the pke package: 
    ``pip install git+https://github.com/boudinfl/pke.git``
4. Download spacy model en_core_web_sm: 
    ``python -m spacy download en_core_web_sm``    
5. Download all necessary nltk packages: 
    * First type in your terminal (with you corresponding python environment): ``python``
    * Type ``import nltk``
    * Type ``nltk.download("all")``
    * Exit python with: ``exit()``
6. Now you can run the app in you python environment by using following command: ``python [PATH TO app.py]``


## Start the Application
In default mode the application runs at localhost with the port 80. After installation you should enter in your 
browser ``localhost:80`` and the application should start. Do guarantee the full functionality you should use Google Chrome. 

![](static/img/git/start_docker.gif)

## Building a Docker Image
The implemented software may be used for later research projects. If you want to build your own docker image you can use
the docker file attached to the code but you can also install the packages directly to you local python distribution if you prefer.
But make sure you copy the docker files outside of the Recommender-System project to build the container. 

The directory structure need to be as followed: 

```
- Dockerfile
- .dockerignore
- Recommender-System
    - data
    - models
    - ...
```

1. Open a terminal and navigate yourself to the directory where you copied the Dockerfile: ``cd [PATH TO Dockerfile]``  
2. Build the image (__This may take a while!__): ```docker build ./ -t rs```  
![](static/img/git/build_docker.gif)  
3. Check if docker installed the container: ``docker ps -a`` (If not execute step 5)  
4. Now you can start and run/stop the docker as usual  
5. Build the container and test it (if necessary): ``docker run --name rs  -p 80:80 rs``  
