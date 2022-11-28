cd d6
ffmpeg -y -f image2 -r 50 -i %%04d.png -vf fps=50 -r 50 -framerate 50 ..\d6.gif