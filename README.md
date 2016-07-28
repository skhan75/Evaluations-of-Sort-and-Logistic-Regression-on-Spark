# Evaluations-on-Spark

###Before running code:
  * Start Spark Cluster
  * Launch Master and Slaves

###1. Running Logistic Regression

1. Copy the LogisticRegression.py file in /spark/bin/
2. Copy DatasetGenerator.py file in your EBS volume or where ever you want to generate your input in. Usually spark creates /vol0 for you.
2. You can use 'vim' to edit DatasetGenerator.py code and change the number of samples you want to generate and again save the file. By default no of samples is kept 100 (n_samples = 100)
3. Now in /vol0 you need to install <b>scikit-learn</b>. Run the following commands:  
    * wget https://bootstrap.pypa.io/get-pip.py  
    * python get-pip.py  
    * pip install --user --install-option="--prefix=" -U scikit-learn  
4. Now generate dataset. Type: python DatasetGenerator.py
5. Go to /root/spark/bin/
6. Run the command below with the following arguments:  
    * ./spark-submit LogisticRegression.py <arg1> <arg2> <arg3> <arg4>
    Here,
      * arg1 -> Input Location (In my case I've my input copied to HDFS)
      * arg2 -> Output Location (same as above)
      * arg3 -> Logisitc Regression Model type (Type either of <b>lgbfs</b> or <b>sgd</b>)
      * arg4 -> Data split percentage for Training without % symbol. 
      * Example: <b>/spark-submit LogisticRegression.py hdfs://ec2-204-236-196-198.compute-1.amazonaws.com:9000/input hdfs://ec2-204-236-196-198.compute-1.amazonaws.com:9000/output1 sgd 80</b>
