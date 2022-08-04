<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
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
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/vonvic/Python-CodeJam-2022-MM">
  </a>

<h2 align="center">Don't Snoop On Me</h3>

  <p align="center">
    A chat app with purposeful misspellings.
    <br />
    <a href="https://youtu.be/SuX59Oc7wz8">View Demo</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li>
      <a href="#how-to-launch">How To Launch</a>
      <ul>
        <li><a href="#the-server">The Server</a></li>
        <li><a href="#a-client">A Client</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#team-members">Team Members</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)
A simple chat app between users with the twist that messages are scrambled but still readable! This is because of the effect of [typoglycemia][typoglycemia-url].

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [![PyQt6][PyQt6-shield]][PyQt6-url]
* [![FastAPI][FastAPI-shield]][FastAPI-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
### Prerequisites
In the terminal, please install dependencies by running
```sh
pip3 install -r dev-requirements.txt
```

<p align="right">(<a href="#top">back to top</a>)</p>

## How To Launch
### The Server
```sh
uvicorn main:app --reload --port 8000
```

### A Client
```sh
python3 client/main.py
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After the server and a client has been launched, the client application will present a prompt to enter a name:
[![Initial][intro-img]

After entering a name and clicking continue, you will then be brought to a new screen. This screen will prompt you to enter a room before you can send any messages. The room ID can be anything, but will be converted to contain no spaces.
[![Initial Main Room][main-empty-img]

Once connected to a room, other users can join the same room with the same ID. From there, you can send each other messages, where received messages will automatically be misspelled.
[![Active Main Room][main-active-img]


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- Members -->
## Team Members
* [Von Vic Cayas](https://github.com/vonvic)
* [tyush](https://github.com/tyush)
* [Firestar](https://github.com/FirestarAD)
* [Jose David Florez Ruiz](https://github.com/J0FR)
* [Max McCready](https://github.com/Bluesquare99)
* [Jaswanth](https://github.com/jasgared)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/vonvic/Python-CodeJam-2022-MM.svg?style=for-the-badge
[contributors-url]: https://github.com/vonvic/Python-CodeJam-2022-MM/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/vonvic/Python-CodeJam-2022-MM.svg?style=for-the-badge
[license-url]: https://github.com/vonvic/Python-CodeJam-2022-MM/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/samples/connected-chat-room.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[typoglycemia-url]: https://en.wikipedia.org/wiki/Transposed_letter_effect
[PyQt6-shield]: https://img.shields.io/badge/pyqt6-016DAD?style=for-the-badge
[PyQt6-url]: https://pypi.org/project/PyQt6/
[FastAPI-shield]: https://img.shields.io/badge/fastpi-009485?style=for-the-badge
[FastAPI-url]: https://fastapi.tiangolo.com/git
[intro-img]: images/samples/initial.png
[main-empty-img]: images/samples/before-connected.png
[main-active-img]: images/samples/connected-chat-room.png
