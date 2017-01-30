# mysql_tpch
This project provides the tools necessary to collect a variety of performance metrics on MySQL with the TPC-H benchmark suite. These tests were done with a single-node setup in all cases. In this README, I will detail the steps necessary to recreate my experiments.

#Setup
##Dependencies
- MySQL

##TPC-H Benchmark Suite on MySQL
1. clone this repo
2. cd into the root directory
3. Build the database of <#>GB size.
  ```
  
  cd dbgen
  mkdir tables
  cd tables
  ../dbgen -s <#>
  ```

#Run
##Query Plan
##IO
##Perf
##PIN

 
