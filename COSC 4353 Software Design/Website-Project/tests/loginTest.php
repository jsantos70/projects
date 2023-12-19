<?php
require_once 'src/login.php';

use PHPUnit\Framework\TestCase;

class loginTest extends TestCase
{
  function testLogin(){
      $conn = mysqli_connect("localhost", "root", "", "fuel");
      if ($conn->connect_error) {
          die("Connection failed: " . $conn->connect_error);
      }
      $uname = 'admin';
      $password = 'apassword';
      $result = login($uname, $password, $conn);
      $this -> assertEquals($result,1);
      $uname = 'huan';
      $password = 'huynh';
      $result = login($uname, $password, $conn);
      $this -> assertEquals($result,2);
      $uname = 'admin';
      $password = '1232password';
      $result = login($uname, $password, $conn);
      $this -> assertEquals($result,3);
      $uname = 'randomaccount';
      $password = 'apassword';
      $result = login($uname, $password, $conn);
      $this -> assertEquals($result,4);
  }
  
}