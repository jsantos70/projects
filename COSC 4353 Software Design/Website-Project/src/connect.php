<?php
    $conn = mysqli_connect("localhost", "root", "", "fuel");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

?>