# A Love Letter to Love Letter - Final Report

A captivating online card game inspired by the classic "Love Letter."

---

## 🚀 Team Members
Our dedicated team of developers and designers:
- **Collin Coakley**
- **Sidney Dean Egan**
- **Harper Chen**
- **Shibo Chen**
- **Roman Di Domizio**

---

## 📌 Quick Links
- **Project Tracker**: [Track our progress and milestones here](https://trello.com/w/thefightingmongooses1/home)
- **GitHub Repository**: [Explore our codebase and commits](https://github.com/CCoakley6/CSPB3308Group5.git)
- **5 Minute Video**: [Watch game demo](https://drive.google.com/file/d/164Yi12JVZb34g67C4Nzt6HPx96tpeJXD/view?usp=drive_link)
- **Public Hosting Site**: [DonutChamp - Play Now!](https://donutchamp.onrender.com/)

---

## 📊 Final Status Report

### 🎉 What We Completed

We have successfully developed a web-based card game that encompasses various components and technologies. The main aspects of our project include:

1. **Front-End Development**: We utilized HTML, CSS, Bootstrap and Javascript to design and create user interface of the game. This includes five main pages:
- **Landing Page**: This page serves as the entry point for users. It contains navigation bars, a welcome section, game rules, a game history table and a link redirecting to `About Us` page. The navigation bars at the top offers links to `Home` page, `Session` page, `About Us` page and our github repository. 
- **Session Page**: This page provides the funtionality for users to create and join game, as well as view existing game sessions.
- **About Us Page**: This page provides information about each team member behind the game and its development process.
- **Game Page**: The core of the application, this page hosts the actual card game for 2 - 4 players, where players can interact and enjoy the gameplay in a specific room.
- **Error Page**: This page could be displayed when users visit non-existent or broken links.

2. **Back-end Development**
- Python served as the primary programming language for the back-end development.
- We employed the Flask framework to build the server-side logic and handle requests from the front-end.
- Flask-SocketIO facilitated the seamless communication between players, enhancing the interactive experience.

3. **Database and Hosting**
- PostgreSQL was chosen as the database system to store relevant game data such as player information, game history, and session information.
- Hosting on Render allows our web application to be publicly accessible and provides a reliable environment for users to access our card game.

Overall, we've successfully brought together various technologies to create a functional web-based card game, encompassing both front-end and back-end components. We're excited to present our game to users and are confident in its functionality and design. 


#### Landing Page
- Designed a visually appealing and intuitive landing page that welcomes players.
- Incorporated dynamic elements to guide users seamlessly into the game.

#### About Us Page
- A dedicated space that shares the info behind our team and the game's creation.

#### Start Button
- A user-friendly 'start' button that transitions players smoothly into gameplay session page.

#### Game Session Page
- The heart of the game where players interact, strategize, and witness the game unfold.

#### Database Setup and Integration
- A robust backend system that efficiently manages game sessions, player data, and more.

#### Game Rendering and Logic
- Brought the game to life with intricate mechanics, ensuring a delightful and challenging experience.

#### Layout Style
- A harmonious and engaging visual theme that resonates with the essence of "Love Letter."

#### Game Page for 2-4 Players
- A versatile game environment that adapts to multiple players, ensuring everyone has a unique experience.

#### Room ID Database
- A secure system that creates private game rooms, ensuring each game session is exclusive.

#### SQL Integration
- Leveraged SQL for swift and reliable interactions with our database.

---

### 🚧 What We Were in the Middle of Implementing
- **Advanced Game Features**: We're introducing exciting power-ups and special cards to spice up gameplay.

---

### 🌟 What We Had Planned for the Future
- **Mobile Responsiveness**: Adapting the game for mobile devices for gaming on-the-go.
- **User Profiles**: Personalized spaces where players can track achievements and customize their gaming experience.
- **Tutorials and Guides**: Helping newcomers grasp the game with interactive walkthroughs.
- **Social Features**: Making it easy to challenge friends and share memorable game moments.
- **Localization**: Bringing the game to a global audience with multiple language options.
- **Sound and Music**: Immersing players with atmospheric sounds and melodies.
- **Chat System**: Enabling players to strategize or simply chat during the game.

---

### ⚠️ Any Known Problems (bugs, issues)
- **Logic Issues**: Some card interactions might play out as expected.
- **Rendering Delays**: Transitioning between game states slower than desired.
- **Database Retrieval Delays**: Peak times might introduce slight delays in data fetching.
- **Mobile Viewport Issues**: We're ironing out some layout quirks on mobile devices.
- **Connection Drops**: We're working on ensuring stable connections for uninterrupted gameplay.
- **Memory Leaks**: We're optimizing our code to prevent potential performance issues during extended play sessions.

