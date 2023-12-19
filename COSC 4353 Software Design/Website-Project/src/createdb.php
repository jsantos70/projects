<?php
$servername = "localhost";
$username = "root";
$password = "";

// Create connection
$conn = new mysqli($servername, $username, $password);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

// Create database
$sql = "CREATE DATABASE fuel";
if ($conn->query($sql) === TRUE) {
  echo "Database fuel created successfully";
} else {
  echo "Error creating database: " . $conn->error;
}
echo "<br>";

$conn->close();

$conn = new mysqli($servername, $username, $password, 'fuel');
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

// sql to create tables
$sql = "CREATE TABLE UserCredentials (
  id int(5) NOT NULL AUTO_INCREMENT,
  username varchar(100) NOT NULL,
	password varchar(255) NOT NULL,
	PRIMARY KEY (id)
)";
if ($conn->query($sql) === TRUE) {
    echo "Fuel Credentials Table created successfully";
} else {
    echo "Error creating table: " . $conn->error;
}

echo "<br>";

$sql = "CREATE TABLE ClientInformation ( 
      id int(5) NOT NULL,
      fullName varchar(100) NOT NULL,
      address_1 varchar(100) NOT NULL,
      address_2 varchar(100),
      state varchar(2) NOT NULL,
      city varchar(50) NOT NULL,
      zipcode int(5) NOT NULL,
      Primary KEY (id),
      FOREIGN KEY (id) REFERENCES UserCredentials(id)
  )";
if ($conn->query($sql) === TRUE) {
    echo "Fuel Client Table created successfully";
  } else {
    echo "Error creating table: " . $conn->error;
  }
  echo "<br>";

$sql="CREATE TABLE FuelQuote (
    orderID int (5) NOT NULL AUTO_INCREMENT,
    userID int(5),
    gallons double NOT NULL,
	  deliveryAdd varchar(200) NOT NULL,
	  deliveryDate date NOT NULL,
	  price double NOT NULL,
	  totalDue double  NOT NULL,
    Primary KEY (orderID),
    FOREIGN KEY (userID) REFERENCES ClientInformation (id)
)";

if ($conn->query($sql) === TRUE) {
  echo "Fuel Quote Table created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

echo "<br>";
  
$conn->close();




?>