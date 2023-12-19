<?php
include('connect.php');
if(!isset($_SESSION)) 
{ 
    session_start(); 
}
function createTable($rows){
    echo "<table class=\"center\" border=1>";  

        foreach($rows as $row){
            echo "<tr>";
            
            echo "<td>".$row['gallons']."</td>";
            echo "<td class = \"address\">".$row['deliveryAdd']."</td>";
            echo "<td class = \"date\">".$row['deliveryDate']."</td>";
            echo "<td>".$row['price']."</td>";
            echo "<td>".$row['totalDue']."</td>";
            
            echo "</tr>";
        }
        echo "</table>";
        return 1;
}
if(!(isset($_SESSION['user']) && isset($_SESSION['id']))){
    header('Location: login.php');
}else if(!(isset($_SESSION['info']))){
    header('Location: profilemanagement.php');
}else{
    $hist = file_get_contents('fuelquoteshistory.html');
    echo $hist;

    $id = $_SESSION['id'];
    $result = mysqli_query($conn,"SELECT * FROM fuelquote WHERE userID=".$id."");

    if(mysqli_num_rows($result)>0){
        while($row = mysqli_fetch_array($result))
        {
            $rows[] = $row;
        }
        createTable($rows);
    }
    
    
    
    
}
?>