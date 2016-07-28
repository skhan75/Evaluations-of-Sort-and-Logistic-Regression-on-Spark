# Evaluations-on-Spark

###Before running code:
  * Start Spark Cluster
  * Launch Master and Slaves

###1. Running Logistic Regression

1. Copy the LogisticRegression.py file in /spark/bin/ (you can use filezilla or putty)
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
      * Example: <b>/spark-submit LogisticRegression.py hdfs://ec2-204-236-196-198.compute-1.amazonaws.com:9000/input hdfs://ec2-204-236-196-198.compute-1.amazonaws.com:9000/output sgd 80</b>
 
###2. Running Terasort

1. Copy the code files in /spark/bin
2. Download Gensort application to generate input for running sort on.
   * wget http://www.ordinal.com/try.cgi/gensort-linux-1.5.tar.gz
   * Go to /64/ 
   * Type ./gensort -a [no_of_Records] [filename.txt]
   * Each line of the record contains 100 bytes
   * So [no_of_Records] * 100 = size of file.
   * Example: ./gensort -a 10000000 pennyInput.txt --> will create a 1GB text file
The sorting is done on keys i.e. first 10 bytes of each records and then the corresponding value is appended.

3. Copy the input to HDFS
   * Go to /root/ephemeral-hdfs/bin 
   * Type:  ./hadoop fs -mkdir /input
   * ./hadoop dfs Ddfs.replication=1 -put /vol0/input /input
   * Copying will take some time depending on the input size

4. Now run the code in spark-shell in /spark/bin/
   * ./spark-shell and press enter
   * This will start the spark shell with scala compiler 
   * Now run the following scala commands linie by line:
      * val lines = sc.textFile("hdfs://ec2-52-38-144-136.us-west-2.compute.amazonaws.com:9000/input") --> give your input location
      * val split = lines.map(x => (x.slice(0,10),x.slice(10,99)))
      * val sort = split.sortByKey()
      * sort.map(k => k._1+k._2).saveAsTextFile("hdfs://ec2-52-38-144-136.us-west-2.compute.amazonaws.com:9000/output") --> your output location
