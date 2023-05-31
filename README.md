# a-star-mazebot
Major Course Output 1 for CSINTSY (Intelligent Systems) class at De La Salle University. An A* Algorithm to solve a given maze. Features a console, web, and desktop GUI.

## **Prerequisites**

Install `Python => version 3.11` & `Pip3`

## **Developing**

Starting Off, in Powershell

```bash
  cd a-star-mazebot
```

## **Running Project**

```bash
  python app.py
```

## Standard Run:
1. Open the source folder and run `app.py`
2. Once ran, you will be prompted with an optional web-based maze animation. (This will generate files in /website)
3. If you choose to generate the web-based animation, an additional web animation will be spawned

### Console Based Legends
- ‘..’ - Road
- ‘##’ -  Wall
- Numbers - Order

### Web App Legends
- White - Road
- Grey - Wall
- Blue  - Visited Road
- Green - Optimal Road
	
### FAQ/Troubleshooting:
- Web Server Unavailable: Another program is using the default assigned server, go to line 194 and change the server to an available one (try 8000). 
- On Web Server - animation is messing up: Reload the web app, when using wait for the current animation to finish before prompting a new one.
- Security prompt on animation - this is because of the webbrowser module (which is completely safe) if you don’t want to give access you can still access the web animation by manually clicking the link in the console (http://localhost:9000/website/index.html)
- The web app isn’t automatically opening up - assuming nothing is broken, it should still be available at the default link http://localhost:9000/website/index.html
- It suddenly stopped working - make sure the console where you ran the file in is still open.
- I want to run a different maze file - go to line 124 in app.py and change the file path
- The input folder or test_mazes folder and the website folder give the error: No such file or directory - Put the said folders outside of the parent folder
- sh: python: command not found - change python to python3

## Desktop GUI Run
1. Go to the `app` folder 
2. Run `gui.py`

### Desktop GUI Legends
- Black - Road
- White - Wall
- Blue  - Visited Road
- Green - Optimal Road
	
### FAQ/Troubleshooting:
- The file won’t run - You are either using an old python version or, for some reason, you do not have the Tkinter toolkit (which should have come with python)
- Can the animation run faster? - Go to lines 28 and 29 of gui.py and change the delay to something faster. 
- I want to run a different maze file - go to line 12 of gui.py and change the file path
- sh: python: command not found - change python to python3


## Screenshots

![App Screenshot](https://github.com/MiguelRobles7/a-star-mazebot/blob/main/screenshots/example_optimal.png)
![App Screenshot](https://github.com/MiguelRobles7/a-star-mazebot/blob/main/screenshots/example_order.png)

## Developers
- [@MiguelRobles7](https://github.com/MiguelRobles7)
- [@qwerttyuiiop1](https://github.com/qwerttyuiiop1)
