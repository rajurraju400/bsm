

# Baby Sleep Monitoring Tool

The Baby Sleep Monitoring Tool is a project designed to help parents monitor the sleep patterns and overall health of their baby. This tool provides a convenient and reliable solution for tracking various sleep-related parameters, allowing parents to gain valuable insights and ensure the well-being of their little ones.

## Features

* Sleep Tracking: The tool enables the recording and analysis of your baby's sleep patterns, including duration, quality, and any disturbances or interruptions.

* Health Monitoring: It provides features to monitor vital health indicators such as heart rate, breathing rate, and body temperature during sleep, helping you keep a close eye on your baby's well-being.

* Notifications: The tool can send timely notifications to alert you about any significant changes or irregularities in your baby's sleep or health, ensuring you stay informed and can take necessary actions promptly.

* Data Visualization: With intuitive and visually appealing graphs and charts, the tool presents sleep and health data in a comprehensive manner, allowing for easy interpretation and analysis.

* Sleep Recommendations: Based on the collected data and established sleep guidelines, the tool can provide personalized recommendations to help improve your baby's sleep habits and promote healthy sleep routines.

## Getting Started
To use the Baby Sleep Monitoring Tool, follow these steps:
```
Clone the repository: git clone https://github.com/rajurraju400/bsm.git
Install the required dependencies: npm install
Configure the tool by specifying your preferences and settings in the appropriate configuration file.
Run the tool: npm start
Access the web interface by opening your browser and navigating to http://localhost:3000.
Begin monitoring your baby's sleep and health by following the on-screen instructions and utilizing the provided features.
```
## Access BSM via Cloud:

* [BSM Cloud UI](http://70.119.111.12:5000/)


## Deploy on your platform locally:

> BSM can be deployed as a container, so prerequisite is you must have docker, podman, cri-o or rocket(anyone) on your platform. I am using docker. FYI. 

#### installation begins:
Check the docker version installed and run the bsm latest container image.

```
[root@fedora ~]# docker --version
Docker version 24.0.2, build cb74dfc
[root@fedora ~]# docker stop bsm
bsm
[root@fedora ~]# docker run -it -d --rm --name bsm -p 5000:5000 bsm bash -c "python3 /bsm/app.py"
66ec1e2d53a2576d761df483894b51a991e765acaa1ceb90f90f5254d586dd5c
[root@fedora ~]#
```

verify the bsm container status

```
[root@fedora ~]# docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                                       NAMES
66ec1e2d53a2   bsm       "bash -c 'python3 /b…"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   bsm
[root@fedora ~]# 
```

#### BSM termination: 

use docker stop to terminate the bsm application on your host

```
[root@fedora ~]# docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                                       NAMES
66ec1e2d53a2   bsm       "bash -c 'python3 /b…"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   bsm
[root@fedora ~]# docker stop bsm
bsm
[root@fedora ~]# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@fedora ~]# 
```

#### Troubleshooting BSM:

check the bsm container logs by running below method:

```[root@fedora ~]# docker logs bsm
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://172.17.0.2:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 487-562-491
[root@fedora ~]# 
```

## Contributing

Contributions to the Baby Sleep Monitoring Tool are welcome! If you'd like to contribute, please follow these guidelines:
```
Fork the repository.
Create a new branch for your feature or bug fix: git checkout -b my-feature.
Make your modifications and commit the changes: git commit -am 'Add new feature'.
Push to the branch: git push origin my-feature.
Submit a pull request, explaining the changes and their benefits.
```
## License
> The Baby Sleep Monitoring Tool is licensed under the MIT License. You are free to use.

## Contact
If you have any questions, suggestions, or feedback regarding the Baby Sleep Monitoring Tool, please don't hesitate to reach out to us. You can contact the project team here.

aparnaraj400@gmail.com - Aparna - Developer of BSM


We hope that this tool helps you in ensuring your baby's sleep and health are carefully monitored, allowing for a more peaceful and confident parenting experience.
