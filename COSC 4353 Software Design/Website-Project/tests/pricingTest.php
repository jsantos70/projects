<?php
require_once 'src/pricingmodule.php';

use PHPUnit\Framework\TestCase;

class pricingTest extends TestCase
{
  function testSuggested(){
    $result = get_suggestedPrice(0.02, 0.01, 0.02);
    $this -> assertEquals($result,1.695);
  }

  function testTotal(){
    $result = get_total(1500, 1.695);
    $this -> assertEquals($result,2542.50);
  }
}