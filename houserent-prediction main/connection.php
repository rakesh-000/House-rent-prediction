<?php
// Create connection
$conn =  mysqli_connect('localhost','root', '','sabarish' );

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
else{
    $username = $_POST['username'];
    $password = $_POST['password'];
    $stmt = $conn->prepare("insert into loginpage(username,password)values(?,?)");
    $stmt->bind_param("ss",$username, $password,);
    $stmt->execute();
    echo "registration SUccessfu\'ly...";
    $stmt->close();
    $conn->close();
}
?>
