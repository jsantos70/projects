<?php
include('connect.php');
include('pricingmodule.php');
if(!isset($_SESSION)) 
{ 
    session_start(); 
}
if(!(isset($_SESSION['user']) && isset($_SESSION['id']))){    
  header('Location: login.php');
}
else if(!(isset($_SESSION['info']))){
  header('Location: profilemanagement.php');
}
$SuggestedPrice = '';
$total = '';

ob_start();
$fuelquoteform = file_get_contents('fuelquoteform.html');
echo $fuelquoteform;

$id = $_SESSION['id'];

$sql_query = "SELECT address_1 FROM clientinformation WHERE id='".$id."' ";
$result=mysqli_query($conn,$sql_query);
$address = mysqli_fetch_array($result)['address_1'];

echo ' <script type="text/javascript">
            document.getElementById("address1").setAttribute("value", "'.$address.'");
        </script>';

//if fuel submit is pressed assign values
if(isset($_POST['butfuelget'])){
    $gallonsrequested = mysqli_real_escape_string($conn, $_POST['requested']);
    $deliveryAdd = mysqli_real_escape_string($conn,$_POST['address1']);
    $deliveryDate = mysqli_real_escape_string($conn,$_POST['deliverydate']);
    
    //if input is not null run
    if ($gallonsrequested != "" && $deliveryAdd != "" && !is_null($deliveryDate)){
      //sql query if in state TX return 1 else 0
      $sql_query = "SELECT id, state FROM clientinformation WHERE state = 'TX' AND id='".$id."' ";
      $result=mysqli_query($conn,$sql_query);

      if(mysqli_num_rows($result)  == 1){
        $LocationFactor=0.02;
      }
      else{
        $LocationFactor=0.04;
      }

      //sql query if there is any previous fuel quote in db
      $result = mysqli_query($conn,"SELECT * FROM fuelquote WHERE userID=".$id."");
      if(mysqli_num_rows($result)!=0){
        $RateHistory=0.01;
      }
      else{
        $RateHistory=0;
      }

      //if gallons more than 1000
      if($gallonsrequested>1000){
        $GallonsFactor=0.02;
      }
      else{
        $GallonsFactor=0.03;
      }
      
      //assign orderid based on number of rows
      $SuggestedPrice = get_suggestedPrice($LocationFactor, $RateHistory, $GallonsFactor);
      $total = get_total($gallonsrequested, $SuggestedPrice);

      $_SESSION['requested']  = $gallonsrequested;
      $_SESSION['date'] = $deliveryDate;
      $_SESSION['address'] = $deliveryAdd;
          
        //output price and total

        echo '
        <script type="text/javascript">
            document.getElementById("suggestedprice").setAttribute("value", '.$SuggestedPrice.');
            document.getElementById("totalamount").setAttribute("value", '.$total.');
        </script>';
        
    }else{
      echo "<p style=\"color:rgb(255,0,0);\">Please fill out all required fields.</p>";
    }
    echo '
    <script type="text/javascript">
    document.getElementById("requested").setAttribute("value", '.$gallonsrequested.');
          document.getElementById("deliverydate").setAttribute("value", "'.$deliveryDate.'");
          </script>';

  }
  //update db
  if(isset($_POST['butfuelsubmit'])){
    $SuggestedPrice =  mysqli_real_escape_string($conn, $_POST['suggestedprice']);
    $total =  mysqli_real_escape_string($conn, $_POST['totalamount']);
    $gallonsrequested = mysqli_real_escape_string($conn, $_POST['requested']);
    $deliveryDate = mysqli_real_escape_string($conn,$_POST['deliverydate']);

    if ($SuggestedPrice != "" && $total != ""){
      mysqli_query($conn, "INSERT INTO fuelquote(userID, gallons, deliveryAdd, deliveryDate, price, totalDue) VALUES (
        '$id', '".$_SESSION['requested']."', '".$_SESSION['address']."',
        '".$_SESSION['date']."', '$SuggestedPrice', '$total')");
      echo '
        <script type="text/javascript">
            document.getElementById("suggestedprice").setAttribute("value", '.$SuggestedPrice.');
            document.getElementById("totalamount").setAttribute("value", '.$total.');
            
        </script>';
        echo "<p style=\"color:rgb(0,255,0);\">Fuel Quote submitted!</p>";
      }else{

        echo "<p style=\"color:rgb(255,0,0);\">Please Get a Quote first.</p>";
      }
      echo '
        <script type="text/javascript">
            document.getElementById("requested").setAttribute("value", '.$_POST['requested'].');
            document.getElementById("deliverydate").setAttribute("value", "'.$_POST['deliverydate'].'");    
        </script>';
  }

?>
