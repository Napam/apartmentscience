[ -z "$PS1" ] && return

export PS1="\[\e[1;35m\]\h\[\e[36m\] \w \[\e[33m\]>\[\e[0m\] "
export TERM=xterm-256color
alias grep="grep --color=auto"
alias ls="ls --color=auto"

echo -e "\e[1;36m"
cat<<EOF
    _   __            __          __
   / | / /___ _____  / /_  ____ _/ /_
  /  |/ / __ \`/ __ \\/ __ \\/ __ \`/ __/
 / /|  / /_/ / /_/ / / / / /_/ / /_
/_/ |_/\\__,_/ .___/_/ /_/\\__,_/\\__/
           /_/
EOF
echo -e "\e[0;33m"

# Turn off colors
echo -e "\e[0m"
