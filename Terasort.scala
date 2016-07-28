// Author: Sami Ahmad Khan
// Course: CS 597 
// Laboratory: DataSys, Illinois Institute of Technology, Chicago, US
// Email: skhan75@hawk.iit.edu
// Description: Terasort on Spark Cluster with varying nodes and workloads

val inputDir = args(0)
val outputDir = args(1)

//Loading input file from HDFS
val lines = sc.textFile(inputDir)
//Splitting the 10 bytes keys and 90 bytes values
val split = lines.map(x => (x.slice(0,10),x.slice(10,99)))
//Sorting rows by Sorting on Keys
val sort = split.sortByKey()
//Saving the output file to HDFS
sort.map(k => k._1+k._2).saveAsTextFile(outputDir)