
# # install oracle java 8
# sudo apt-get purge openjdk*   # just in case
# sudo apt-get install software-properties-common
# sudo add-apt-repository ppa:webupd8team/java
# sudo apt-get update
# sudo apt-get install oracle-java8-installer

# install openjdk-7 
#sudo apt-get purge openjdk*
#sudo apt-get -y install openjdk-7-jdk

# check java version
java -version
# java version "1.7.0_65"

# install curl
#sudo apt-get -y install curl

echo "# Downloading the elasticsearch setup"
# install Elasticsearch 1.3.2
wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.2.deb
sudo dpkg -i elasticsearch-2.0.0-rc1.deb
rm elasticsearch.tar.gz

#test the installation
sudo /etc/init.d/elasticsearch start
curl localhost:9200
sudo /etc/init.d/elasticsearch stop

echo "# Starting the elasticsearch service"
# start ES service
sudo /bin/systemctl start elasticsearch.service


# # test ES
# curl localhost:9200
# curl -XGET http://127.0.0.1:9200/_cluster/health?pretty
# curl -XGET http://localhost:9200/_cluster/state/nodes?pretty


# install ES HQ
cd /usr/local/share/elasticsearch/
./bin/plugin -install royrusso/elasticsearch-HQ

# http://localhost:9200/_plugin/HQ/

# # stop ES service
# sudo service elasticsearch stop


# # directories
# /usr/local/share/elasticsearch

echo "# Installing python es client"
# install pip and the python ES client
sudo apt-get -y install python-setuptools
sudo easy_install pip
sudo pip install elasticsearch