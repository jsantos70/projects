<?php
require_once 'src/profilemanagement.php';

use PHPUnit\Framework\TestCase;

class profileTest extends TestCase
{
  function testNewProf(){
      $conn = mysqli_connect("localhost", "root", "", "fuel");
      if ($conn->connect_error) {
          die("Connection failed: " . $conn->connect_error);
      }
      
      $result = newProf(2, 'Huan', '12','', "houston", 'tx', '77077',$conn);
      $this -> assertEquals($result,1);
  }

  function testEditProf(){
    $conn = mysqli_connect("localhost", "root", "", "fuel");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    
    $result = editProf(3, 'Huan', '12345','', "houston", 'tx', '77077',$conn);
    $this -> assertEquals($result,1);

    }
    
}