<?php
include "connect.php";
if(!isset($_SESSION)) 
{ 
    session_start(); 
}
if(isset($_SESSION['user']) && isset($_SESSION['id'])){
    header('Location: home.php');
}
function login($uname, $password, $conn){
    $sql_query = "SELECT id, password FROM usercredentials WHERE username='".$uname."'";
    $result=mysqli_query($conn,$sql_query);
    
    if(mysqli_num_rows($result)  == 1){
        $account=mysqli_fetch_array($result);
        $hashed_password = $account['password'];
        if(password_verify($password, $hashed_password)){
            $id=$account['id'];
            
            $result = mysqli_query($conn,"SELECT * FROM clientinformation WHERE id=".$id."");
            $rows=mysqli_fetch_array($result);

            if(mysqli_num_rows($result) == 0){
                $_SESSION['id'] = $id;
                $_SESSION['user'] = $uname;
                return 1;
            }else{
                $_SESSION['id'] = $id;
                $_SESSION['user'] = $uname;
                $_SESSION['info'] = $rows;
                return 2;
            }
        }else{

            return 3;
        }
    }else{
        return 4;
    }
}
ob_start();
$login = file_get_contents('login.html');
echo $login;

if(isset($_GET['message'])){
    echo "<p style=\"color:rgb(0,255,0);\">".$_GET['message']."</p>";
}

if(isset($_POST['butlogin'])){
    $uname = mysqli_real_escape_string($conn,$_POST['username']);
    $password = mysqli_real_escape_string($conn,$_POST['password']);
                
    if ($uname != "" && $password != ""){
        $process = login($uname,$password,$conn);
        switch($process){
            case 1:
                header('Location: profilemanagement.php');
                
                ob_end_flush();
                break;
            case 2:
                header('Location: home.php');
                
                ob_end_flush();
                break;
            case 3:
                echo "<p style=\"color:rgb(255,0,0);\">Incorrect password.</p>";
                break;
            case 4:
                echo "<p style=\"color:rgb(255,0,0);\">Invalid username.</p>";
                break;
        }
    }
        
}

?>