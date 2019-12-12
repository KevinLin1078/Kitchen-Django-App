# git clone --single-branch --branch kevin https://github.com/beseidel/kitchen

echo "To install application, type 2" 
echo -e "Option: \c"
read error


if [ $error == 2 ]
then 
   sudo apt-get update
   sudo apt-get install python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python3-pip -y
   sudo apt-get install libmysqlclient-dev -y
   echo "y" | sudo ufw enable

   sudo apt-get update
   sudo pip3 install virtualenv 
   virtualenv ~/env
   source ~/env/bin/activate
   ~/env/bin/pip3 install -r install.txt
   ~/env/bin/pip3 install django-paypal
   sudo apt-get update
   
   sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y
   sudo ufw allow 'Apache Full'
   sudo ufw allow 'OpenSSH'
   sudo ufw allow '3000'
   sudo ufw allow '80'
   sudo apt-get install curl
   curl -4 icanhazip.com
   file=/etc/apache2/sites-enabled/000-default.conf
   if [ -e $file ]
   then 
      sudo rm /etc/apache2/sites-enabled/000-default.conf
   fi
   sudo cp ~/kitchen/apache.conf /etc/apache2/sites-enabled/
   sudo service apache2 restart
   


fi