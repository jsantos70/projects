<?php
require_once 'src/registeration.php';

use PHPUnit\Framework\TestCase;

class registerTest extends TestCase
{
  function testReg(){
      $conn = mysqli_connect("localhost", "root", "", "fuel");
      if ($conn->connect_error) {
          die("Connection failed: " . $conn->connect_error);
      }
      $uname = (string)uniqid('user_');
      $password = 'apassword';
      $result = register($uname, $password, $conn);
      $this -> assertEquals($result,1);
      
      $uname = 'admin';
      $password = 'apassword';
      $result = register($uname, $password, $conn);
      $this -> assertEquals($result,3);
      $uname = 'randomaccount';
      $password = 'pass';
      $result = register($uname, $password, $conn);
      $this -> assertEquals($result,4);
      
      $uname = random_bytes(5);
      $password = 'apassword';
      $result = register($uname, $password, $conn);
      $this -> assertEquals($result,2);
  }
}