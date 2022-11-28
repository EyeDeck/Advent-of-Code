cd d3
ffmpeg -y -f image2 -r 50 -i frame%%04d.png -vf fps=50 -r 50 -framerate 50 ..\d3.gif