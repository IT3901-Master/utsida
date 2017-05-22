# Utsida

## Installation Guide

### Prerequisite programs

**Java 8**
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer

**Python3 and Pip3**
sudo apt-get install python3                                       
sudo apt-get install python3-pip                                   
**Git**
sudo apt-get install git                                          


**Download both required Git repositories**
git clone https://github.com/IT3901-Master/utsida.git              
git clone https://github.com/IT3901-Master/mycbr-deployment.git    


**Setup and run**
sudo pip3 install -r requirements.txt
make initiate
make lrun

