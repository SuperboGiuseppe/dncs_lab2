<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/SuperboGiuseppe/dncs_lab2">
    <img src="Images/network.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">AUTOMATING THE DEPLOYMENT OF NETWORK SETUPS USING VAGRANT</h3>

  <p align="center">
    Design of Networks and communication systems - Project A.Y. 2020-21 University of Trento, Italy
    <br />
    <a href="https://github.com/SuperboGiuseppe/dncs_lab2"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/SuperboGiuseppe/dncs_lab2/blob/main/README.md">View Demo</a>
    ·
    <a href="https://github.com/SuperboGiuseppe/dncs_lab2/issues">Report Bug</a>
    ·
    <a href="https://github.com/SuperboGiuseppe/dncs_lab2/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#List-of-features">List of features</a></li>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#Dashboard">Dashboard</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-Requirements">Installation Requirements</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
   </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Main window screenshot][product-screenshot]

This project is based on a graphical user interface (GUI) that provides a platform for the developer to create a fully automated virtual network environment for testing and development. The users can easily customize and design a virtual network environment according to their needs. With the help of this platform, a user can create and configure different virtual machines acting as a server, router, switches, and hosts or specialized hosts. Custom topologies can be designed from scratch or starting from predefined templates. Once the network is deployed and configured, the user can access or monitor each virtual machine.

### Dashboard

A monitoring dashboard is configured and deployed in order to provide users an extended view of the single virtual machine status. The configuration of the dashboard is based on a specific data flux which is commonly adopted in network configurations:
- **Telegraf** collects data from the target node and sends it to a specific end-point via http requests;
- **Influxdb** receives the data from the target node and stores it in an optimal way;
- **Grafana** plots and prompts the data stored in influxdb through a custom dashboard.

![Dashboard data flux scheme][dashboard-flux]
![Dashboard example CPU][dashboard-cpu]
![Dashboard example network][dashboard-network]

The configuration of this flux is automated as, everytime a network is deployed, an additional vagrant environment is deployed in "Dashboard_server". The machine where grafana server is executed is based on the following Vagrant Box: [superbogiuseppe/grafana_server](https://app.vagrantup.com/superbogiuseppe/boxes/grafana_server).

Credentials for the dashboard:
    - Username: admin
    - Password: dashboard

### List of features
Available features:
- Provide Graphical User Interface for creating Virtual environments;
- provide a modern monitoring architecture to monitor running virtual environments;
- Provide the functionality to use different Linux machine's flavors for different purposes;
- Provide the option to set a specific uplink or downlink speed limit;
- Provide the option to control your network in real-time;
- Provide the option to write and debug the vagrant scripts;
- Provide the option of customizing the network topologies;
- Provide the option of using different Docker images.

### Built With

A network is composed of a set of computing devices connected to each other. Likewise, a graph is a mathematical structure composed of a set of nodes connected among each other via edges. For this reason, the network management core of this project is based on a really light python library called pyvis, which is based on javascript. This library, makes it possible to have a very clear network visualization and all the details of each node collected in the entity itself. In order to monitor the network statistics, we have used (Telegraf, InfluxBD, and Grafana). These technologies are open source and easy to use and implement. They also provide an open platform for beautiful analytics and monitoring (a dashboard for displaying data) from many sources, particularly time-series data. On the backend, we have used the vagrant development environment by HashiCorp along with the VirtualBox. Vagrant is a simple and powerful tool that provides a platform where we can easily integrate our existing configuration management toolings like Ansible, Chef, Docker, Puppet, or Salt. 

* [Pyvis](https://pyvis.readthedocs.io/en/latest/tutorial.html)
* [Vagrant](https://www.vagrantup.com/)
* [QtPy](https://pypi.org/project/PyQt5/)
* [Vagrant Boxes](https://app.vagrantup.com/boxes/search)
* [Python](https://www.python.org/)
* [VirtualBox](https://www.virtualbox.org/)
* [Html](https://en.wikipedia.org/wiki/HTML#:~:text=Hypertext%20Markup%20Language%20(HTML)%20is,scripting%20languages%20such%20as%20JavaScript.)
* [Docker](https://www.docker.com/)
* [OpenSwitch](https://www.openswitch.net/)
* [Quagga Routing](https://www.quagga.net/)
* [Wondershaper](https://github.com/magnific0/wondershaper)
* [Grafana](https://grafana.com/)
* [Influxdata](https://www.influxdata.com/products/influxdb-overview/)
* [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/)

These tools have not been used in the default topologies that we have created. But users can create and configure custom topologies using these tools easily.
* [Ansible](https://www.ansible.com/)
* [Puppet](https://puppet.com/)
* [Salt](https://saltproject.io/automating-network-operations-with-salt-2019-2-0/)

<!-- GETTING STARTED -->
## Getting Started

In order to get benefit from this environment, you must have some basic knowledge of networking, python, vagrant configuration, etc.

### Prerequisites

Some prerequisites have to be done before using this environment. It's based on your operating system. You can use Windows, Mac, Linux, but you have to see the procedure of installation according to your operating system.  We have used the entire windows operating system to develop this environment. But anyone can install it on the other operating system.

<!--
* npm
  ```sh
  npm install npm@latest -g
  ``
-->

### Installation Requirements

1. [Python 3.9.0](https://www.python.org/)
    - [pyvis](https://pyvis.readthedocs.io/en/latest/install.html#install-with-pip) (pip install pyvis)
    - [PyQt5](https://pypi.org/project/PyQt5/) (pip install pyqt5)
    - [PyYAML](https://pypi.org/project/PyYAML/) (pip install pyyaml)
    - [ipcalc](https://pypi.org/project/ipcalc/) (pip install ipcalc)
2. 10GB disk storage
3. Windows/Linux/Mac
4. [VirtualBox](https://www.virtualbox.org/)
5. [Vagrant](https://www.vagrantup.com/)
6. Internet
7. Clone the repo
   ```sh
   git clone https://github.com/SuperboGiuseppe/dncs_lab2.git
   ```
<!-- USAGE EXAMPLES -->
## Usage

This project is only used to provide the user to test their environments by providing the same operating system, packages, and configurations, all while giving users the flexibility to use their favorite editor, IDE, and browsers. In order to launch the design tool, execute the following command in the main directory of the project:
   ```sh
   python ./main.py
   ```

### Create a new network
By pressing "New network", a wizard will be prompted. Here it is possible to create a network from scratch (**Not currently implemented**) or to create a network from a template. Once the template has been selected, the same topology will be available on the main canvas and ready to be configured/modified/deployed.

### Save network
By pressing "Save network", it is possible to save the network in a html format (Pyvis compatible format) along with its configuration.

### Open network
By pressing "Open network", it is possible to import an already configured/designed network. It is necessary that the file is compatible with the pyvis library (HTML format).

### Adding new devices (**Not currently implemented**)
By pressing the buttons "Router", "Switch", "Host" or "Other", it is possible to add a new device to the network.

### Edit configuration
By pressing "Edit configuration" it is possible to edit the configuration of each device of the network:
  - Virtual machine characteristics (CPUs, RAM, VM Image, device name);
  - Network configuration of each interface (IP, Netmask, interface name);
  - Custom script to be provisioned during the deployment.

### Edge configuration
By pressing "Edge configuration", it is possible to edit uplink and downlink speed limits of each edge.

### Deploy network
By pressing "Deploy network", the network will be deployed via Vagrant. It is recommended to have the debug console active in order to retrieve any deployment error or warning.

### Control dashboard
Once the network is deployed successfully, by pressing "Control dashboard", it is possible to navigate in the grafana interface in order to visualize any real-time statistic of each machine.

### SSH Connection
By pressing "SSH Connection", it is possible to establish an SSH connection with a specific node of the deployed network: a terminal will be prompted once the connection has been established.

### Debug console
By pressing "Debug console", it is possible to show/hide the debug console which is useful during the deployment phase of the network.

### Turn on/off VMs
By pressing "Turn on/of VMs", it is possible to stop all the devices of the network without destroying them.

### Destroy network
By pressing "Destroy network", it is possible to destroy the deployed network along with the dashboard server.


<!-- _For more examples, please refer to the [Documentation](https://www.vagrantup.com/docs)_ >



<!-- ROADMAP -->
## Roadmap
The road map we have:
- On the Frontend python library called pyvis used.
- On the backend vagrant scripts used to create the virtual machines.
- On the backend, we have created a mechanism that converts the Vagrant scripts into the HTML formats in order to be compatible with the pyvis.
- A virtual machine created separately to manage the dashboard that runs along automatically with vagrant topologies. 


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin Feature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project coordinator
- [Professor Fabrizio Granelli](https://github.com/fabrizio-granelli)

Students
- [Giuseppe Superbo](https://github.com/SuperboGiuseppe)
- [Luca Staboli](https://github.com/LucaStabo)
- [Muhammad Uzair](https://github.com/uzairali37)

Project Link: [AUTOMATING THE DEPLOYMENT OF NETWORK SETUPS USING VAGRANT](https://github.com/SuperboGiuseppe/dncs_lab2)



<!-- ACKNOWLEDGEMENTS
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)
 -->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/SuperboGiuseppe/dncs_lab2.svg?style=for-the-badge
[contributors-url]: https://github.com/SuperboGiuseppe/dncs_lab2/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SuperboGiuseppe/dncs_lab2.svg?style=for-the-badge
[forks-url]: https://github.com/uzairali37/dncs_lab2
[stars-shield]: https://img.shields.io/github/stars/SuperboGiuseppe/dncs_lab2.svg?style=for-the-badge
[stars-url]: https://github.com/SuperboGiuseppe/dncs_lab2/stargazers
[issues-shield]: https://img.shields.io/github/issues/SuperboGiuseppe/dncs_lab2.svg?style=for-the-badge
[issues-url]: https://github.com/SuperboGiuseppe/dncs_lab2/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[product-screenshot]: Images/Documentation/screenshot.png
[dashboard-flux]: Images/Documentation/dashboard_flux.png
[dashboard-cpu]: Images/Documentation/Dashboard_2.png
[dashboard-network]: Images/Documentation/Dashboard_1.png
