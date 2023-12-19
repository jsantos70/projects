<?php
if(!isset($_SESSION)) 
{ 
    session_start(); 
}
include("connect.php"); 
if(isset($_SESSION['user']) && isset($_SESSION['id'])){
    header('Location: home.php');
}

function register($username, $passwd, $conn){
    if ( strlen($passwd) >= 5 && strpbrk($passwd, "!#$.,:;()") == false ){
        //query and check if username is not in database
        $hashed_password =  password_hash($passwd, 
        PASSWORD_BCRYPT);
        $query = mysqli_query($conn, "SELECT * FROM usercredentials WHERE username='{$username}'");
        //assigns id based on number of rows in database

        if (mysqli_num_rows($query) == 0){
            //insert into database
            mysqli_query($conn, "INSERT INTO usercredentials(username,password) VALUES (
                '$username',  '$hashed_password')");
            
            // verify the user's account was created
            $query = mysqli_query($conn, "SELECT * FROM usercredentials WHERE username='{$username}'");
            
            if (mysqli_num_rows($query) == 1){
                
                return 1;
            }
            else
                
                return 2;
        }
        else
    
            return 3;
        
        }
    else
       
       return 4;
    }

ob_start();
$reg = file_get_contents('registeration.html');
echo $reg;

    $username="";
    $passwd="";
    //if registerbutton clicked assign values
    if (isset($_POST['registerBtn'])){ 
        $username = $_POST['username']?? ''; 
        $passwd = $_POST['password']?? '';
        

        //if username and password arent empty
        if ($username != "" && $passwd != ""){
            // make sure the password is above 5 characters and dont include illegal characters
            $process = register($username,$passwd,$conn);
            switch($process){
                case 1:
                    header('Location: login.php?message=Account created succesfully.');      
                    ob_end_flush();    
                    break;
                case 2:
                    echo "<p style=\"color:rgb(255,0,0);\">An error occurred and your account was not created.</p>";
                    break;
                case 3:
                    echo "<p style=\"color:rgb(255,0,0);\">The username <i>'$username'</i> is already taken. Please use another.</p>";
                    break;
                case 4:
                    echo "<p style=\"color:rgb(255,0,0);\">Your password is not strong enough. Please use another.</p>";
                    break;
            }
    }
}
    

?>