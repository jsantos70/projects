<?php
include('connect.php');
if(!isset($_SESSION)) 
{ 
    session_start(); 
}

function newProf($id, $fullname, $firstaddress,$secondaddress, $city,$state, $zipcode,$conn){
    mysqli_query($conn, "INSERT INTO clientinformation VALUES (
        '$id',  '$fullname', '$firstaddress', '$secondaddress',
        '$state', '$city', '$zipcode')");

    $result = mysqli_query($conn,"SELECT * FROM clientinformation WHERE id=".$id."");
    $rows=mysqli_fetch_array($result);
    if (mysqli_num_rows($result) !=0){
        $_SESSION['info'] = $rows;
        return 1;        
    }
    else{
        
        return 2;
    }
}

function editProf($id, $fullname, $firstaddress,$secondaddress, $city, $state, $zipcode,$conn){
    mysqli_query($conn, "UPDATE clientinformation Set 
        fullName='$fullname', address_1='$firstaddress', address_2='$secondaddress',
        state='$state', city='$city', zipcode='$zipcode' WHERE id =".$id."");

        $result = mysqli_query($conn,"SELECT * FROM clientinformation WHERE id=".$id."");
        $rows=mysqli_fetch_array($result);

        if (mysqli_num_rows($result) !=0){     
            $_SESSION['info'] = $rows;
            return 1;     
        }
        else{
            return 2;
        }
}

if(!(isset($_SESSION['user']) && isset($_SESSION['id']))){    
    header('Location: login.php');
}else{


$profile = file_get_contents('profilemanagement.html');
echo $profile;

    if(isset($_POST['butprofileset'])){
        
        $fullname = mysqli_real_escape_string($conn,$_POST['fullName']);
        $firstaddress = mysqli_real_escape_string($conn,$_POST['address1']);
        $secondaddress = mysqli_real_escape_string($conn,$_POST['address2']);
        $city = mysqli_real_escape_string($conn,$_POST['city']);
        $state = mysqli_real_escape_string($conn,$_POST['state']);
        $zipcode= mysqli_real_escape_string($conn,$_POST['zipcode']);
        
        if ($fullname != "" && $firstaddress != ""&& $city != ""&& $state != ""&& $zipcode != "" ){
            $id = $_SESSION['id'];
            if(!(isset($_SESSION['info']))){
               $process = newProf($id, $fullname, $firstaddress,$secondaddress, $city, $state, $zipcode,$conn);
               switch($process){
                    case 1:
                        echo "<p style=\"color:rgb(0,255,0);\">Succesfully edited profile!</p>";
                        break;
                    case 2:
                        echo "<p style=\"color:rgb(255,0,0);\">An error occurred and your profile was not edited.</p>";
                        break;
               }     
                
            }else{
                $process = editProf($id, $fullname, $firstaddress,$secondaddress, $city, $state, $zipcode,$conn);
                switch($process){
                    case 1:
                        echo "<p style=\"color:rgb(0,255,0);\">Succesfully edited profile!</p>";
                        break;
                    case 2:
                        echo "<p style=\"color:rgb(255,0,0);\">An error occurred and your profile was not edited.</p>";
                        break;
               }     
            }
        }
        
    }
}

?>
