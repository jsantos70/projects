<?php
require_once 'src/fuelquoteshistory.php';

use PHPUnit\Framework\TestCase;

class historyTest extends TestCase
{
  function testTable(){
      $conn = mysqli_connect("localhost", "root", "", "fuel");
      if ($conn->connect_error) {
          die("Connection failed: " . $conn->connect_error);
      }
      $result = mysqli_query($conn,"SELECT * FROM fuelquote WHERE userID=14");
      while($row = mysqli_fetch_array($result))
      {
          $rows[] = $row;
      }
      $result = createTable($rows);
      
      $this -> assertEquals($result,1);
  }

 
}