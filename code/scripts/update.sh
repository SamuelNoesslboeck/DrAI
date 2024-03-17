echo
echo "  DrAI - Update batch file"
echo ============================
echo -> ATTENTION: This script must be executed from the projects root folder!
echo
echo Checking for updates in the main repo ...
echo

git fetch
# git checkout master
git pull origin

echo
echo Checking for updates in the submodules ...
echo

git submodule update --init --recursive

echo