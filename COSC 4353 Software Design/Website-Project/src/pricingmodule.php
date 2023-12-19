<?php
  // Methods
  function get_suggestedPrice($LocationFactor, $RateHistory, $GallonsFactor){
    //constants
    $CurrentPrice=1.5;
    $CompanyProfitFactor=0.1;
    //calculations
    $Margin= $CurrentPrice * ($LocationFactor - $RateHistory + $GallonsFactor + $CompanyProfitFactor);
    $SuggestedPrice = $CurrentPrice + $Margin;

    return $SuggestedPrice;
  } 

  function get_total($gallonsrequested, $SuggestedPrice){
    $total=$gallonsrequested*$SuggestedPrice;
    return $total;
  }



?>