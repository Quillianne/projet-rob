message=$(cat prompt.txt)
echo "$message" | xclip -selection clipboard

# zone +
xdotool mousemove 652 1013
xdotool click 1
# zone upload image
sleep 0.2
xdotool mousemove 653 948
xdotool click 1
#picture
sleep 0.3
xdotool mousemove 602 472
xdotool click 1

#documents
#sleep 0.2
#xdotool mousemove 402 359
#xdotool click 1

#bouton recherche
sleep 0.2
xdotool mousemove 1285 197
xdotool click 1
sleep 0.5
xdotool type --delay 500 "porte_2"
xdotool mousemove 800 312
sleep 3
xdotool click 1
sleep 0.05
xdotool click 1
#taper la commande
sleep 0.5
xdotool mousemove 717 1017
sleep 0.2
xdotool click 1
sleep 0.2
xdotool key ctrl+v
xdotool key Return

xclip -selection clipboard /dev/null

#attendre la réponse
sleep 8
#copier le texte répondu
xdotool mousemove 600 941
xdotool click 1
sleep 0.1
xdotool key End
sleep 0.1
xdotool key End
xdotool mousemove 715 941
sleep 1
#clique sur le presse papier pour copier
xdotool click 1
sleep 0.1
xdotool click 1
sleep 1
sleep 0.1
reponse=$(xsel --clipboard --output -o)
sleep 1
echo "le texte copié est : $reponse"

