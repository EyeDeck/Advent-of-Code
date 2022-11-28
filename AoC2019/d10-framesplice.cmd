cd d10
ffmpeg -y -f image2 -r 50 -i frame%%06d.png -vf fps=50 -r 50 -framerate 50 ..\d10.gif